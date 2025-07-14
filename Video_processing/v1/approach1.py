import yt_dlp
import easyocr
import cv2
import cv2
import numpy as np
import os
from google import genai
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



# Initialize the reader with English language


# Perform OCR

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


def getfull_text(frame_dir):
    full_txt=""
    #get all the text
    for filename in os.listdir(frame_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            image_path = os.path.join(frame_dir, filename)
            print(f"extracting from frame {image_path}")
            full_txt+=easy_ocr(image_path)
    
    return full_txt


def correctwithllm(instruction):

            client = genai.Client(api_key=API_KEY)
    
            instruction=getfull_text("./")
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=f"this text is extracted from screenshots of code , can you write the code section correctly and ignore what is not code:this is the code {instruction}"
            )
            return response.text





