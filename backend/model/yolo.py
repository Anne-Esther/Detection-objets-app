import torch
import cv2

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def detect_objects(image_path):
    results = model(image_path)
    results.render()
    img = results.ims[0]
    return cv2.imencode('.jpg', img)[1].tobytes()
