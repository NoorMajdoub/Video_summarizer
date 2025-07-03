from dotenv import load_dotenv
from audio_processing import get_transcript

import os
import json
import google.generativeai as genai
import asyncio
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
MODEL_NAME= os.getenv("MODEL_NAME")

genai.configure(api_key=api_key)
def get_prompttext(text):
                prompt_visual = f"""
                You are an expert technical summarizer and knowledge graph builder.

                Given the following text:

                {text}

                Perform the following tasks with clear and structured output:

                1. **Entities**  
                List all the key entities mentioned in the text. Present them as a bullet list or table. Include entity types where possible (e.g., Person, Organization, Technology, etc.).

                2. **Relations**  
                Identify and describe the relationships between the entities. Present them as triples in the format:  
                **[Entity 1]—[Relation]—[Entity 2]**

                Ensure the output is clean, easy to read, and grouped under clear section headers.
                """

                res=prompt_visual.format(text=text)
        
                return res
def get_graph(text):
    temp=text.split("Relations**")[1]
    temp=temp.split("*")
    temp=[[t.split("—")[0],t.split("—")[1],t.split("—")[2]] for t in temp if t.strip()!="" and len(t.split("—"))==3]
    
    return temp
async def get_visual_summary(vid_url,vid_input=None):

    model = genai.GenerativeModel(MODEL_NAME)
    chat = model.start_chat()
    #get dat transcription babayyyyyyy
    text=get_transcript(vid_url)
    instruction =get_prompttext(text)
   
    response = await chat.send_message_async(instruction)
    result = response.text

  
    return result

