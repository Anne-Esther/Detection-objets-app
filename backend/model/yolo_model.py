import torch

# Charge le modèle nano (2MB) au lieu de 'yolov5s' (14MB)
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)

def predict_image(image_path):
    results = model(image_path)
    return {
        "detections": results.pandas().xyxy[0].to_dict('records'),
        "count": len(results.xyxy[0])
    }
