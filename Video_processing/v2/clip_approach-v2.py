import yt_dlp
import easyocr
import cv2
import cv2
import numpy as np
import os
from dotenv import load_dotenv
import os
import easyocr
import cv2
import google.generativeai as genai
import asyncio
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import glob
import os

load_dotenv() 

api_key = os.getenv("GOOGLE_API_KEY")
MODEL_NAME= os.getenv("MODEL_NAME")

genai.configure(api_key=api_key)

#function to locally download the video
def download_vid(name, url):
    ydl_opts = {
        'outtmpl': f'downloaded_video{name[:3]}.%(ext)s',
        'format': 'bestvideo[ext=mp4]+bestaudio/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'cookies': '/kaggle/input/cookies3/www.youtube.com_cookies (1).txt',
        'ignoreerrors': True,
        'retries': 10,
        'fragment_retries': 10,
        # Avoid AV1 formats
        'format_sort': ['+codec:h264,+codec:vp9'],
        'prefer_free_formats': False,
        'extractor_args': {
            'youtube': {
                'skip': ['dash', 'hls']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
#function to extract frames randomly accordking to the interval we set here the interval is every 50 sec

def get_frames(video_path):
        capture = cv2.VideoCapture(video_path)
        timestamps=[]

        if not capture.isOpened():
            print("Error opening video file.")
            exit()

        fps = capture.get(cv2.CAP_PROP_FPS)
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        interval = 50  # seconds
        for sec in range(0, int(duration), interval):
            frame_number = int(sec * fps)
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            success, frame = capture.read()
            cv2.imwrite(f"frame{sec}.png", frame)
            print(f"saved frame{sec}")
            if not success:
                print(f"Failed to read frame at {sec} seconds.")
                continue



        capture.release()



# Inputs
def iscodeframe(path):
        image = Image.open(path).convert("RGB")
        text_prompts = ["a screenshot of code", "a code editor", "a terminal with code","code"] #added code
        
        inputs = processor(text=text_prompts, images=image, return_tensors="pt", padding=True)
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        image_embeds = outputs.image_embeds  # shape: [1, 512]
        text_embeds = outputs.text_embeds    # shape: [3, 512]
        similarity = (image_embeds @ text_embeds.T).squeeze()
        if similarity.max().item() > 0.3:  # tune later
                    print("Code detected ",similarity.max().item())
                    return True
        else:
            print("nocode",similarity.max().item())
            return False
        
        #get the frames of code 
def getcodetimestamps():

        code=[]
        output_dir = '/kaggle/working/'
        pattern = os.path.join(output_dir, 'd*')  



        files = glob.glob(pattern)

        for image_path in files:
            if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                print(f"Processing frame {image_path}")
                output=iscodeframe(image_path)
                if output:
                    code.append(image_path)
                print(output)
                return code
        
      
def get_code_intervals(timestamps,code):
    intervals=[]
    for c in code:
            c=int(c[c.index("d")+1:c.index(".")])
            
            for i in range(len(timestamps) - 1):
                if timestamps[i][1] == c:
                    print("bingo")
                    intervals.append((timestamps[i][1], timestamps[i + 1][0]))
    return intervals


def re_get_frames(intervals):
            video_path = "/kaggle/working/downloaded_videodes.mp4"  
            capture = cv2.VideoCapture(video_path)
            timestamps=[]
            if not capture.isOpened():
                  print("Error opening video file.")
                  exit()
                            
            fps = capture.get(cv2.CAP_PROP_FPS)
            frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps
            jump = 10  # make later % to length of interval 
            for inter in intervals:
                    for sec in range(inter[0], inter[1], jump):
                        frame_number = int(sec * fps)
                        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                        success, frame = capture.read()
                        cv2.imwrite(f"code{sec}.png", frame)
                        print(f"saved frame{sec}")
                        if not success:
                            print(f"Failed to read frame at {sec} seconds.")
                            continue
                    
                    
                    
            capture.release()





# main OCR function

def easy_ocr(image):
  reader = easyocr.Reader(['en'])
  data=""
  image = cv2.imread(image)
  try:
    result = reader.readtext(image)
    for _, text, _ in result:
         data+=text
    return data
  except:
   return data

#now that we got alll the section that have code lets get the stupid code 
def getstupidcode():
        code=""
        output_dir = '/kaggle/working/'
        pattern = os.path.join(output_dir, 'code*')  # all files starting with d



        files = glob.glob(pattern)

        for image_path in files:
            if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                print(f"Processing frame {image_path}")
                code+=easy_ocr(image_path)
        return code
        
if __name__=="__main__":
     model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
     processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

     