
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    return parse_qs(parsed.query).get("v", [None])[0]

def get_transcript(url_vid):
    id_vid = get_video_id(url_vid)
    ytt = YouTubeTranscriptApi()
    transcript = ytt.fetch(id_vid)
    tran_joined = " ".join((entry.text for entry in transcript))
    return tran_joined