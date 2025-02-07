from fastapi import FastAPI, Body

app = FastAPI()

@app.post("/upload-audio/")
async def upload_audio(file_bytes: bytes = Body(...)):
    # Process received bytes
    file_size = len(file_bytes)

    return {"message": "File received, ok!", "size_in_bytes": file_size}
