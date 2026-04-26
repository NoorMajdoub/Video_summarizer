import os
import uvicorn
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
 
from audio_processing import get_transcript
from summary import get_textual_summary
from visual_summary import get_visual_summary, get_graph
from prompt2dict import prompt_2_json
 
load_dotenv()
 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



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
    transcript = get_transcript(data.vid_url)
 
    # Run both summaries using the same transcript
    textual_result = await get_textual_summary(transcript)
    visual_result = await get_visual_summary(transcript)
 
    # Parse textual summary into structured dict
    parsed = prompt_2_json(textual_result)
 
    # Parse visual result into graph triples
    parsed["visual"] = get_graph(visual_result)
 
    return parsed
 
 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)