from pydantic import BaseModel
from visual_summary import get_graph, get_visual_summary
from summary import get_textual_summary
from audio_processing import get_transcript
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai
import asyncio
from prompt2dict import prompt_2_json
from fastapi import FastAPI,Query
from fastapi.middleware.cors import CORSMiddleware

load_dotenv() 

api_key = os.getenv("GOOGLE_API_KEY")
MODEL_NAME= os.getenv("MODEL_NAME")

genai.configure(api_key=api_key)
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
    res2=await get_visual_summary(data.vid_url)
    res2=get_graph(res2)
    res=prompt_2_json(result)
    #result="why god"
    res["visual"]=res2
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)