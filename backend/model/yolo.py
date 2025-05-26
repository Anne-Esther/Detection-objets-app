import torch
import cv2

# Charger le modèle localement (depuis le chemin dans le repo)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='backend/model/yolov5s.pt')

def detect_objects(image_path):
    results = model(image_path)
    results.render()
    img = results.ims[0]
    return cv2.imencode('.jpg', img)[1].tobytes()
