"""
main.py
Main backend code for starting the server and setting up the endpoints
"""
import os
import uvicorn
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pyngrok import conf
from pyngrok import ngrok
import asyncio
from video_processing import *
from summary import *
from visual_summary import *
from prompts import 
from prompt2dict import 

load_dotenv()
auth_token = os.getenv("ngrok_auth_token")
conf.get_default().auth_token =auth_token

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
  

class VideoRequest(BaseModel):
    vid_url: str

@app.get("/")
def read_root():
    return {"message": "Video Summarizer API is running."}


@app.post("/summarize")
async def summarize(data: VideoRequest):

    # Fetch transcript once — reused by both summary and visual
    transcript = get_transcript(data.vid_url)  #gets transcript fine
 
    # Run both summaries using the same transcript
    textual_result = await get_textual_summary(transcript)
    visual_result = await get_visual_summary(transcript)
 
    # Parse textual summary into structured dict
    parsed = prompt_2_json(textual_result)
 
    # Parse visual result into graph triples
    parsed["visual"] = get_graph_nlp(transcript) 
 
    return parsed
 
 
@app.post("/getcode")
async def getcode(data: VideoRequest):
    code = code_extraction_pipeline("dest",data.vid_url)
    return {"code": code}


# --- server startup ---
if __name__ == "__main__":
    nest_asyncio.apply()
    public_url = ngrok.connect(8001)
    print("Backend URL:", public_url)
    config = uvicorn.Config(app, host="0.0.0.0", port=8001)
    server = uvicorn.Server(config)
    asyncio.run(server.serve())
