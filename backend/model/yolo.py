import torch
import cv2
import os

# chemin relatif vers le modèle local
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'yolov5s.pt')

# charger le modèle local YOLOv5 (mode eval)
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH, source='local')
model.eval()

def detect_objects(image_path):
    results = model(image_path)  # détecte les objets
    results.render()  # dessine les boîtes sur l'image
    img = results.ims[0]
    # encode en jpg
    return cv2.imencode('.jpg', img)[1].tobytes()
