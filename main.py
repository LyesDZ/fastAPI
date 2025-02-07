from fastapi import FastAPI, File, UploadFile
from io import BytesIO
import shutil

app = FastAPI()

@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    # Create a BytesIO stream to hold the uploaded audio
    audio_bytes = BytesIO(await file.read())
    
    # Optionally save the file to disk (for testing purposes)
    with open(f"{file.filename}", "wb") as f:
        shutil.copyfileobj(audio_bytes, f)

    return {"filename": file.filename, "message": "File uploaded successfully!"}
