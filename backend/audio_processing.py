
from youtube_transcript_api import YouTubeTranscriptApi


# get id of the youtube video 
def get_video_id(url):
    return url.split("watch?v=")[-1]

def get_transcript(url_vid):
    id_vid=get_video_id(url_vid)
    transcript = YouTubeTranscriptApi.get_transcript(id_vid)
   # frames=get_frames(transcript)
    tran_joined=" ".join((line["text"] for line in transcript))
    return tran_joined
