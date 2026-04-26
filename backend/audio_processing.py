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

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig
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
    username = os.getenv("WEBSHARE_USERNAME")
    password = os.getenv("WEBSHARE_PASSWORD")
    # using a specific free proxy IP from your list
    proxy_url = f"http://{username}:{password}@198.23.239.134:6540"
    proxy_config = GenericProxyConfig(
        http_url=proxy_url,
        https_url=proxy_url
    )
    ytt = YouTubeTranscriptApi(proxy_config=proxy_config)
    transcript = ytt.fetch(id_vid)
    tran_joined = " ".join((entry.text for entry in transcript))
    return tran_joined