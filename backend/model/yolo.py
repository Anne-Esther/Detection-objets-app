import torch
import cv2
from pathlib import Path

# Obtenir le dossier du fichier courant (model/yolo.py)
current_dir = Path(__file__).parent

# Construire le chemin absolu vers le fichier yolov5s.pt
model_path = current_dir / 'yolov5s.pt'

# Charger le modèle depuis le chemin absolu
model = torch.hub.load('ultralytics/yolov5', 'custom', path=str(model_path))

def detect_objects(image_path):
    results = model(image_path)
    results.render()
    img = results.ims[0]
    return cv2.imencode('.jpg', img)[1].tobytes()

