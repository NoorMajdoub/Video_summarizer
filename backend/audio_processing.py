from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv

load_dotenv()

def get_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    return parse_qs(parsed.query).get("v", [None])[0]

def get_transcript(url_vid):
    id_vid = get_video_id(url_vid)
    proxy_config = WebshareProxyConfig(
        proxy_username=os.getenv("WEBSHARE_USERNAME"),
        proxy_password=os.getenv("WEBSHARE_PASSWORD"),
        proxy_scheme="http"  # force HTTP
    )
    ytt = YouTubeTranscriptApi(proxy_config=proxy_config)
    transcript = ytt.fetch(id_vid)
    tran_joined = " ".join((entry.text for entry in transcript))
    return tran_joined