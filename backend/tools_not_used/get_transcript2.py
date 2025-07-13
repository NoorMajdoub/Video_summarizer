import yt_dlp
import speech_recognition as sr

from pydub import AudioSegment



def get_transcript(url):


        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        audio = AudioSegment.from_mp3("audio.mp3")
        audio.export("audio.wav", format="wav")

        recognizer = sr.Recognizer()
        with sr.AudioFile("audio.wav") as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        return text
