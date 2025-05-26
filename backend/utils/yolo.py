import torch
import os
from pathlib import Path

# Chargement sécurisé du modèle YOLO
def load_model():
    try:
        # Chemin absolu vers le modèle
        model_dir = Path(__file__).parent / "model"
        model_path = model_dir / "yolov5s.pt"
        
        # Vérification de l'existence du fichier
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        # Chargement avec vérification du device
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = torch.hub.load('ultralytics/yolov5', 'custom', 
                             path=str(model_path), 
                             force_reload=False,
                             device=device)
        
        # Configuration du modèle
        model.eval()
        model.conf = 0.5  # Seuil de confiance
        model.iou = 0.45  # Seuil d'intersection
        
        return model
    
    except Exception as e:
        raise RuntimeError(f"Error loading YOLO model: {str(e)}")


# Fonction de prédiction optimisée
def predict_image(model, image_path):
    try:
        # Vérification de l'image
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")
            
        # Prédiction
        results = model(image_path)
        
        # Formatage des résultats
        return {
            "detections": results.pandas().xyxy[0].to_dict('records'),
            "success": True
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }
