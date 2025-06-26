
from audio_processing import get_transcript
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai
import asyncio
load_dotenv() 

api_key = os.getenv("GOOGLE_API_KEY")
MODEL_NAME= os.getenv("MODEL_NAME")

genai.configure(api_key=api_key)

#get text summary == get sth we will write to the user
text=""
prompt_text=f"""

You are an expert technical summarizer and knowledge graph builder.

Given the following text:

{text}

Do the following:

1. **Goal**: Clearly state the main objective or purpose of the text in in 1-2 sentences.

2. **Global Understanding**: Summarize the high-level idea of what is being explained or taught, in 2-4 sentences.

3. **Steps (if any)**: If the text contains steps, procedures, or sequential logic, list them clearly in order. Use bullet points.

4. **Entity Extraction**:
   - Identify all unique entities or concepts mentioned in the text.
   - Organize them into the following categories:
     - People : list them and present the role of each 
     - Tools / Libraries / Technologies : list them and present what we used them for
     - Actions / Tasks
     - Output / Results
   - Present them as bullet points under each category."""

async def get_textual_summary(vid_url,instruction=prompt_text,vid_input=None):

    model = genai.GenerativeModel(MODEL_NAME)
    chat = model.start_chat()
    response = await chat.send_message_async(instruction)
    result = response.text

  
    return result


if __name__ == "__main__":

      #text=get_transcript("https://www.youtube.com/watch?v=Tw18-4U7mts")
      #print(text)
      #print(f"{MODEL_NAME}   -- {api_key}")
      result =asyncio.run(get_textual_summary("kjk","hi bunbun"))
      print(result)