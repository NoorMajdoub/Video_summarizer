"""
Video_processing.py
Main code for extracting the code from the video
"""
import yt_dlp
import cv2
from PIL import Image
import torch
import numpy as np
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import random
import os
import easyocr
import cv2
from difflib import SequenceMatcher
from prompts import get_code_cleaning_prompt

def code_extraction_pipeline(name,vid_url):
    model,processor=get_model()
    print("----------------Downloading the video------------")
    download_vid(name, vid_url)  #the url the user puts
    print("----------------Getting time stanmps------------")

    time_stamps=get_timestamps("/kaggle/working/downloaded_videodes.mp4") #the video path is after it is downladed
    print("----------------Getting code intervals------------")

    code_intervals=detect_code_intervals(time_stamps,model,processor)
    print("----------------getting the code with ocr------------")

    code=get_code_with_ocr(code_intervals)
    print("--------------Cleaning code with LLM-----------------")
    clean_code=call_llm(get_code_cleaning_prompt(code))
    return clean_code
    
def download_vid(name, url):
    ydl_opts = {
        'outtmpl': f'downloaded_video{name[:3]}.%(ext)s',
        'format': 'bestvideo[ext=mp4]+bestaudio/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'cookies': '/kaggle/input/cookies3/www.youtube.com_cookies (1).txt',
        'ignoreerrors': True,
        'retries': 10,
        'fragment_retries': 10,
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
        
def get_histogram(image):
    """
    Gets image and returns histogram
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
    cv2.normalize(hist, hist)
    return hist
    
def format_time(sec):
    minutes = sec // 60
    seconds = sec % 60
    return f"{minutes}:{seconds:02d}"
    
def get_timestamps(video_path):
            """
            Function to get the timestamps of the video , by sampling the video (every 3 seconds) and comparing the changes in
            histogram to detect changes in the frame
            Args:
                Input : video path (after it is downloaded , it is fixed because the backend is running on kaggle)
            Returns:
                Array of timestamps
            """
            
            capture = cv2.VideoCapture(video_path)
            timestamps=[]
            
            if not capture.isOpened():
                print("Error opening video file.")
                exit()
            
            fps = capture.get(cv2.CAP_PROP_FPS)
            frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps
            #initialise last frame with the first frame in the vid
            _, frame0 = capture.read()
            last_frame=frame0
            last_check=0
            last_save=0
            #timestamps.append(last_frame)
            cv2.imwrite(f"m{last_check}.png", last_frame)
            interval = 3  # seconds
            
            for sec in range(0, int(duration), interval):
                frame_number = int(sec * fps)
                capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                success, frame = capture.read()
                diff = cv2.compareHist(get_histogram(last_frame), get_histogram(frame), cv2.HISTCMP_BHATTACHARYYA)
            
                if diff > 0.6:  #threshold to detect the changes in frames
                    timestamps.append((format_time(last_save), format_time(sec)))
                    print(format_time(sec))
                    cv2.imwrite(f"d{sec}.png", frame)  # boundary frame
                    last_save = sec
            
                cv2.imwrite(f"all{sec}.png", frame)  # save every frame regardless
                
                last_frame = frame
                last_check = sec
                if not success:
                    continue
            
            capture.release()
            return timestamps
    
def get_model():
    """
    The clip model used to detect code
    """
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor



def isCodeFrame(image_path,model,processor):
    """
    Function to return True/False of presence of code in a frame
    Uses 3 Prompts(the texts) embeddings to get the logits of matching #TODO improve description
    Args:
        Input: image , model , processor
    Returns :
        Probs of matching of the image with each of the three text promtps
    """
    image = Image.open(image_path).convert("RGB")
    w, h = image.size
    image = image.crop((0, 0, int(w * 0.85), int(h * 0.85)))
    
    text_prompts = [
        "programming code in a text editor",
        "a slide presentation",
        "a person or abstract background"
    ]
    inputs = processor(text=text_prompts, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    
    probs = outputs.logits_per_image.softmax(dim=-1).squeeze()
    
    print(f"code:{probs[0]:.3f} slide:{probs[1]:.3f} other:{probs[2]:.3f}  ---{image_path}")
    return probs[0].item() > 0.9  #higher threshold to be sure 

def detect_code_intervals(timestamps,model,processor, interval=3):
    """
    Function that will run the code detection approach on the timestamps to detect which are of code
    Runs is_code function on the beginning of the interval , the end ,and two random frames from the middle
    If 2/4 of the frames are of code, then the interval is detected to contain code 
    """
    code_intervals = []
    
    for begin, end in timestamps:
        begin_sec = time_to_sec(begin)
        end_sec = time_to_sec(end)
        
        # pick 2 random frames guaranteed to have saved files
        mid_range = list(range(begin_sec + interval, end_sec - interval, interval))
        if len(mid_range) >= 2:
            mid1_sec, mid2_sec = random.sample(mid_range, 2)
        else:
            mid1_sec = begin_sec
            mid2_sec = end_sec
        
        begin_path = f"/kaggle/working/all{begin_sec}.png"
        end_path   = f"/kaggle/working/all{end_sec}.png"
        mid1_path  = f"/kaggle/working/all{mid1_sec}.png"
        mid2_path  = f"/kaggle/working/all{mid2_sec}.png"
        
        res_beg  = isCodeFrame(begin_path,model,processor)
        res_mid1 = isCodeFrame(mid1_path,model,processor)
        res_mid2 = isCodeFrame(mid2_path,model,processor)
        res_end  = isCodeFrame(end_path,model,processor)
        
        votes = [res_beg, res_mid1, res_mid2, res_end]
        print(f"{begin}-{end} | {votes} | sum={sum(votes)}")
        
        if sum(votes) >= 2:
            code_intervals.append((begin, end))
    
    return code_intervals

def time_to_sec(t):
    parts = t.split(":")
    return int(parts[0]) * 60 + int(parts[1])

def is_duplicate(new_text, seen_texts, threshold=0.85):
    for seen in seen_texts:
        if SequenceMatcher(None, new_text, seen).ratio() > threshold:
            return True
    return False
def easy_ocr(image,reader):
      """
      Helper funcction to apply the ocr on the image
      """
      data=""
      image = cv2.imread(image)
      try:
        result = reader.readtext(image)
        for _, text, _ in result:
             data+=text
        return data
      except:
       return data
def get_code_with_ocr(code_intervals):
        """
        Gets the code from the code intervals 
        Args:
            The code intervals timestamps
        Returns :
            all the code extracted in one array
        
        """
        all_code = []
        seen_texts = []
        reader = easyocr.Reader(['en'])

        for begin, end in code_intervals:
            begin_sec = time_to_sec(begin)
            end_sec = time_to_sec(end)
            
            if end_sec - begin_sec <= 15:
                print(f"skipping {begin} to {end} — too short")
                continue
            print(f"\n--- Extracting code from {begin} to {end} ---")
        
            for sec in range(begin_sec, end_sec, 6):
                path = f"/kaggle/working/all{sec}.png"
                if not os.path.exists(path):
                    continue
                
                text = easy_ocr(path,reader)
                
                if not text.strip():
                    continue
                
                if not is_duplicate(text, seen_texts):
                    seen_texts.append(text)
                    all_code.append(text)
        
        final_code = '\n\n'.join(all_code)
        return final_code
