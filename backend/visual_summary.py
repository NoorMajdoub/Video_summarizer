"""
visual_summary.py
Generates entity-relation knowledge graph data from a video transcript using Gemini.
"""
 
import os
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import get_visual_prompt
 
load_dotenv()
 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_NAME = os.getenv("MODEL_NAME")



def get_graph(text):
    try:
        if "Relations" not in text:
            return []
 
        relations_section = text.split("Relations")[1]
        parts = relations_section.split("*")
 
        triples = []
        for part in parts:
            part = part.strip()
            if not part:
                continue
            segments = part.split("—")
            if len(segments) == 3:
                triple = [s.strip() for s in segments]
                triples.append(triple)
 
        return triples[:4]
 
    except Exception as e:
        print(f"[visual_summary] get_graph parsing failed: {e}")
        return []


async def get_visual_summary(transcript):
    model = genai.GenerativeModel(MODEL_NAME)
    chat = model.start_chat()
    response = await chat.send_message_async(get_visual_prompt(transcript))
    return response.text
 
