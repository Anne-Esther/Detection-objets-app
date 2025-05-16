from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from model.yolo import detect_objects
import shutil, io

app = FastAPI()

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    with open("backend/input.jpg", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result_img = detect_objects("backend/input.jpg")
    return StreamingResponse(io.BytesIO(result_img), media_type="image/jpeg")
