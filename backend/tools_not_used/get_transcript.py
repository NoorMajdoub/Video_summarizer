import yt_dlp

url = "https://www.youtube.com/watch?v=zc5NTeJbk-k"



ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'audio.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
import whisper

model = whisper.load_model("base")  
result = model.transcribe("audio.mp3")

print(result['text'])
