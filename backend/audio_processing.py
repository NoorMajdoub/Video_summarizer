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
    Function to get the transcript of a youtube video using yt_dlp
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

    with open(vtt_path, 'r', encoding="utf-8") as f:
        lines = f.readlines()

    seen = set()
    clean_lines = []
    for line in lines:
        line = line.strip()
        if (not line or
            '-->' in line or
            line.startswith('WEBVTT') or
            line.startswith('Kind:') or
            line.startswith('Language:') or
            line in seen):
            continue
        seen.add(line)
        clean_lines.append(line)
    
    text = " ".join(clean_lines)
    text = re.sub(r'<[^>]+>', '', text)

    text = re.sub(r' +', ' ', text).strip()
    return text
