from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch
import shutil
from pathlib import Path
from PIL import Image
import io
import os

app = FastAPI()

# CORS pour autoriser le frontend Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplace * par ton URL Vercel en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger le modèle localement
model_path = Path(__file__).parent / "models" / "yolov5s.pt"
model = torch.hub.load('ultralytics/yolov5', 'custom', path=str(model_path), force_reload=False)

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    results = model(image)

    # Sauvegarder l'image avec les boîtes détectées
    output_path = f"static/detected_{file.filename}"
    results.save(save_dir="static")

    return JSONResponse(content={"result": f"/{output_path}"})

