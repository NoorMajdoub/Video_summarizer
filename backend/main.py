
"""
main.py
Main backend code for starting the server and setting up the endpoints
"""

import os
import shutil
import nest_asyncio
import uvicorn
import google as genai
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel

from pyngrok import conf
from pyngrok import ngrok

from kaggle_secrets import UserSecretsClient

from video_processing import *
from summary import *
from visual_summary import *
import prompts
import prompt2dict
from graph_store import VideoGraphStore
from qa_agent import answer_question
from audio_processing import *


# ============================================================
# KAGGLE FILE PATHS
# ============================================================

# /kaggle/input is READ-ONLY.
# Copy cookies.txt to /kaggle/working so yt-dlp can update it.
SOURCE_COOKIES = "/kaggle/input/datasets/isramoussaoui/coding/backend/cookies.txt"
WORKING_COOKIES = "/kaggle/working/cookies.txt"

if os.path.exists(SOURCE_COOKIES):
    shutil.copy2(SOURCE_COOKIES, WORKING_COOKIES)
    print(f"Cookies copied to: {WORKING_COOKIES}")
else:
    print(f"WARNING: Cookies file not found: {SOURCE_COOKIES}")


# Make these available to video_processing.py
os.environ["VIDEO_COOKIES_FILE"] = WORKING_COOKIES
os.environ["VIDEO_WORK_DIR"] = "/kaggle/working"


# ============================================================
# NGROK AUTHENTICATION
# ============================================================

user_secrets = UserSecretsClient()

# Kaggle Secret must be named exactly:
# NGROK_AUTHTOKEN
auth_token = user_secrets.get_secret("NGROK_AUTHTOKEN")

conf.get_default().auth_token = auth_token


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI()


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# GRAPH STORE
# ============================================================

graph_store = VideoGraphStore()


# ============================================================
# REQUEST MODELS
# ============================================================

class VideoRequest(BaseModel):
    vid_url: str


class AskRequest(BaseModel):
    vid_url: str | None = None
    question: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def read_root():
    return {
        "message": "Video Summarizer API is running."
    }


# ============================================================
# SUMMARIZE ENDPOINT
# ============================================================

@app.post("/summarize")
async def summarize(data: VideoRequest):

    # Fetch transcript once.
    # NOTE: get_transcript / get_graph_nlp are synchronous, blocking calls.
    # Running them directly in this coroutine freezes the *entire* server's
    # single event loop for their duration -- including unrelated requests
    # like /ask. run_in_threadpool offloads them to a worker thread so other
    # requests can still be served concurrently.
    transcript = await run_in_threadpool(get_transcript, data.vid_url)

    # Generate textual summary
    textual_result = await get_textual_summary(transcript)

    # Generate visual summary


    # Parse textual summary into structured JSON
    parsed = prompt2dict.prompt_2_json(textual_result)

    # Generate visual graph information (spaCy + sentence-transformers --
    # synchronous and can take a few seconds; offload it too)
    parsed["visual"] = await run_in_threadpool(get_graph_nlp, transcript)

    # Persist the video's structured summary and triples
    # into Neo4j. Also synchronous network I/O -- offload.
    try:
        await run_in_threadpool(
            graph_store.store_video_summary,
            data.vid_url,
            parsed,
            parsed["visual"],
        )

    except Exception as e:
        print(
            f"[graph_store] failed to persist summary: {e}"
        )

    # Chunk + embed the transcript so /ask can semantically search it.
    try:
        await run_in_threadpool(
            graph_store.store_segments,
            data.vid_url,
            transcript_text=transcript,
        )

    except Exception as e:
        print(
            f"[graph_store] failed to persist transcript segments: {e}"
        )

    return parsed


# ============================================================
# GET CODE ENDPOINT
# ============================================================

@app.post("/getcode")
async def getcode(data: VideoRequest):

    # Extract code from the video -- by far the heaviest call in the whole
    # app (download + CLIP + OCR + LLM cleanup, often minutes). Definitely
    # offload this or it blocks every other request for the whole duration.
    code = await run_in_threadpool(
        code_extraction_pipeline,
        "dest",
        data.vid_url,
    )

    # Attach extracted code to the video's graph node
    try:
        await run_in_threadpool(
            graph_store.store_video_summary,
            data.vid_url,
            {},
            [],
            code=code,
        )

    except Exception as e:
        print(
            f"[graph_store] failed to persist code: {e}"
        )

    # Chunk + embed the OCR'd code so /ask can semantically search it
    # alongside the transcript.
    try:
        await run_in_threadpool(
            graph_store.store_segments,
            data.vid_url,
            code_text=code,
        )

    except Exception as e:
        print(
            f"[graph_store] failed to persist code segments: {e}"
        )

    return {
        "code": code
    }


# ============================================================
# ASK ENDPOINT
# ============================================================

@app.post("/ask")
async def ask(data: AskRequest):
    """
    Answer a question grounded in the persisted graph.
    """

    # answer_question does Neo4j reads, sentence-transformer encoding, and
    # a Groq LLM call -- all synchronous. Offload so a slow /ask doesn't
    # block other in-flight requests either.
    result = await run_in_threadpool(
        answer_question,
        data.question,
        graph_store,
        vid_url=data.vid_url,
    )

    return result


# ============================================================
# SERVER STARTUP
# ============================================================

if __name__ == "__main__":

    # Required for running async code in Kaggle
    nest_asyncio.apply()

    # --------------------------------------------------------
    # Clean up existing ngrok tunnels
    # --------------------------------------------------------

    try:
        ngrok.kill()
        print("Existing ngrok tunnels cleaned up.")
    except Exception as e:
        print(f"Could not clean up ngrok tunnels: {e}")

    # --------------------------------------------------------
    # Start ngrok
    # --------------------------------------------------------

    try:
        tunnel = ngrok.connect(
            addr=8001,
            proto="http"
        )

        public_url = tunnel.public_url

        print()
        print("=" * 60)
        print("NGROK TUNNEL")
        print("=" * 60)
        print(f"Backend URL: {public_url}")
        print("=" * 60)
        print()

    except Exception as e:
        print()
        print("=" * 60)
        print("NGROK FAILED")
        print("=" * 60)
        print(e)
        print("=" * 60)
        print()

        # Stop here because the frontend needs the public URL
        raise

    # --------------------------------------------------------
    # Start Uvicorn / FastAPI
    # --------------------------------------------------------

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8001
    )

    server = uvicorn.Server(config)

    asyncio.run(server.serve())
