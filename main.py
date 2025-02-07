import os
from fastapi import FastAPI, Body
from groq import Groq  # Make sure you have `groq` installed: pip install groq

app = FastAPI()

# Load API Key from Environment Variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing! Set it as an environment variable.")

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

def get_transcription(client, audio_bytes):
    """
    Transcribes an audio file using Groq Whisper API.
    - `audio_bytes`: Raw audio data in bytes.
    """
    transcription = client.audio.transcriptions.create(
        file=("recording.wav", audio_bytes),
        model="whisper-large-v3",
        response_format="verbose_json",
    )
    return transcription.text

@app.post("/transcribe-audio/")
async def transcribe_audio(file_bytes: bytes = Body(...)):
    """
    Receives raw audio bytes, sends them to Groq for transcription, 
    and returns the transcribed text.
    """
    transcript_text = get_transcription(client, file_bytes)
    return {"transcription": transcript_text}
