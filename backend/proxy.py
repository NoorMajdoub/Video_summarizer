from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

# Replace with your actual proxy credentials
proxy_username = "sixmnprb"
proxy_password = "qbxzbaf94qsm"
proxy_host = "proxy.webshare.io"  # or whatever your proxy host is
proxy_port = 5868  # or the correct port (e.g., 8000, 3128)

# Set up proxy config
proxy_config = WebshareProxyConfig(
   
    proxy_port=proxy_port,
    proxy_username=proxy_username,
    proxy_password=proxy_password
)

# Create API instance with proxy
ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)

# Extract video ID from URL
def get_video_id(url):
    return url.split("watch?v=")[-1]

video_url = "https://www.youtube.com/watch?v=nFoXCLi8FCc"
video_id = get_video_id(video_url)

# Fetch transcript
transcript = ytt_api.get_transcript(video_id)
print(transcript)
