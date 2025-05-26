import torch
import os

def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "model", "yolov5s.pt")
    model = torch.load(model_path, map_location=torch.device('cpu'))
    model.eval()
    return model
