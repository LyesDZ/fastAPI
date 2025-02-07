import os
import io
from fastapi import FastAPI, Body, HTTPException
from groq import Groq

app = FastAPI()

# Load API Key
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
    if not audio_bytes:
        raise ValueError("No audio data received!")

    # Wrap bytes in a file-like object (Groq may require this)
    file_like = io.BytesIO(audio_bytes)

    transcription = client.audio.transcriptions.create(
        file=("recording.wav", file_like),
        model="whisper-large-v3",
        response_format="verbose_json",
    )
    
    return transcription.text

@app.post("/transcribe-audio/")
async def transcribe_audio(file_bytes: bytes = Body(...)):
    """
    Receives raw audio bytes, validates them, and sends them to Groq for transcription.
    """
    if not file_bytes:
        raise HTTPException(status_code=400, detail="No audio data received!")

    print(f"Received {len(file_bytes)} bytes of audio data.")

    try:
        transcript_text = get_transcription(client, file_bytes)
        return {"transcription": transcript_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
