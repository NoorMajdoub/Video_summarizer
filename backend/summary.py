"""
summary.py
Generates a structured textual summary of a YouTube video using Gemini.
"""
 
import os
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import get_summary_prompt
 

load_dotenv() 
api_key = os.getenv("GOOGLE_API_KEY")
MODEL_NAME= os.getenv("MODEL_NAME")

genai.configure(api_key=api_key)


async def get_textual_summary(transcript):
    """
    Generates a structured textual summary from a video transcript.
    Args:
        transcript: Plain text transcript of the video (fetched once in main.py).
    Returns:
        Structured summary as a raw string from Gemini.
    """
    model = genai.GenerativeModel(MODEL_NAME)
    chat = model.start_chat()   
    response = await chat.send_message_async(get_summary_prompt(transcript))
    return response.text


