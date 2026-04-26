from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv
import yt_dlp
from urllib.parse import urlparse, parse_qs
load_dotenv()





def get_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    return parse_qs(parsed.query).get("v", [None])[0]

def get_transcript(url_vid):
    ydl_opts = {
        'skip_download': True,  # don't download video
        'writeautomaticsub': True,  # get auto-generated subtitles
        'writesubtitles': True,
        'subtitleslangs': ['en'],
        'subtitlesformat': 'vtt',
        'outtmpl': '/tmp/transcript',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url_vid])
    
    # read the downloaded subtitle file
    with open('/tmp/transcript.en.vtt', 'r') as f:
        lines = f.readlines()
    
    # strip vtt formatting, keep only text
    text = " ".join(
        line.strip() for line in lines 
        if line.strip() and '-->' not in line and not line.startswith('WEBVTT')
    )
    return text
