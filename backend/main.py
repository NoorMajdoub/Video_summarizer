from pydantic import BaseModel
from summary import get_textual_summary
from audio_processing import get_transcript
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai
import asyncio

from fastapi import FastAPI,Query
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

class VideoRequest(BaseModel):
    vid_url: str

@app.post("/summarize")
async def get_text_summary(data: VideoRequest):
    result = await get_textual_summary(data.vid_url)
    return result

if __name__ == "__main__":
    import uvicorn
    #print(GEMINI_API_KEY)
    uvicorn.run(app, host="0.0.0.0", port=8001)