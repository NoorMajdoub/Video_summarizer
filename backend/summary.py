"""
summary.py
Generates a structured textual summary of a YouTube video using LLM.
"""
 
from llm_call import call_llm
from prompts import get_summary_prompt


async def get_textual_summary(transcript):
    """
    Generates a structured textual summary from a video transcript
    Args:
        transcript: Plain text transcript of the video (fetched once in main.py)
    Returns:
        Structured summary as a raw string from the llm used
    """
    res=call_llm(get_summary_prompt(transcript)) 
   # print(res)
    return res
