import os
import tempfile
import re
import yt_dlp
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
 
load_dotenv()


#audio processing.py


def get_video_id(url):
    """
    Function to Extracts the YouTube video ID from a full URL.
    """
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    return parse_qs(parsed.query).get("v", [None])[0]


def get_transcript(url_vid):
    """
    Function to get the transcript of a youtube video.
    Uses yt_dlp
    Args:
        url_vid: Full YouTube video URL.
    Returns:
        Transcript as a single plain text string.
    Raises:
        FileNotFoundError: If no English subtitles were found for the video.
    """
    tmp_dir = tempfile.gettempdir()
    output_path = os.path.join(tmp_dir, "transcript")  #folder to save transcript in
    vtt_path = os.path.join(tmp_dir, "transcript.en.vtt")
    ydl_opts = {
        'skip_download': True,  # don't download video
        'writeautomaticsub': True,  # get auto-generated subtitles
        'writesubtitles': True,
        'subtitleslangs': ['en'],
        'subtitlesformat': 'vtt',
        'outtmpl': output_path,
         "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url_vid])

    if not os.path.exists(vtt_path):
        raise FileNotFoundError(
            f"No English subtitles found for this video. "
            f"Make sure the video has auto-generated captions enabled."
        )

    # We read the downloaded subtitle file
    with open(vtt_path, 'r',encoding="utf-8") as f:
        lines = f.readlines()
    
    #  vtt formatting to extract the text only
    text = " ".join(
        line.strip() for line in lines 
        if line.strip() and '-->' not in line and not line.startswith('WEBVTT')
    )
    return text
