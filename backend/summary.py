"""
summary.py
Generates a structured textual summary of a YouTube video using LLM.
"""
 
import os
import google.generativeai as genai
from dotenv import load_dotenv
from llm_call import call_llm



load_dotenv()
async def get_textual_summary(transcript):
    """
    Generates a structured textual summary from a video transcript.
    Args:
        transcript: Plain text transcript of the video (fetched once in main.py).
    Returns:
        Structured summary as a raw string from Gemini.
    """
    res=call_llm(get_summary_prompt(transcript)) 
    print(res)
    return res
