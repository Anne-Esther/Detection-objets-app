import torch
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Union

# Configuration globale
MODEL_PATH = Path(__file__).parent / "yolov5s.pt"
CONFIDENCE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.45

class YOLOModel:
    def __init__(self):
        self.model = None
        self.device = self._get_device()
        
    def _get_device(self):
        """Détecte automatiquement le meilleur device (GPU/CPU)"""
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    def load_model(self):
        """Charge le modèle YOLO avec gestion d'erreur"""
        try:
            if not MODEL_PATH.exists():
                raise FileNotFoundError(f"Fichier modèle introuvable: {MODEL_PATH}")
                
            self.model = torch.hub.load(
                'ultralytics/yolov5', 
                'custom',
                path=str(MODEL_PATH),
                device=self.device
            )
            
            # Configuration des paramètres
            self.model.conf = CONFIDENCE_THRESHOLD
            self.model.iou = IOU_THRESHOLD
            self.model.eval()
            
            return self
            
        except Exception as e:
            raise RuntimeError(f"Erreur de chargement du modèle: {str(e)}")

    def predict(self, image_path: Union[str, Path]) -> Dict:
        """Effectue une prédiction sur une image"""
        try:
            # Vérification de l'image
            if not Path(image_path).exists():
                raise ValueError("Le fichier image n'existe pas")
            
            # Lecture de l'image
            img = cv2.imread(str(image_path))
            if img is None:
                raise ValueError("Impossible de lire l'image")
            
            # Prédiction
            results = self.model(img)
            
            # Formatage des résultats
            detections = results.pandas().xyxy[0].to_dict('records')
            
            return {
                "success": True,
                "detections": detections,
                "image_size": {"width": img.shape[1], "height": img.shape[0]},
                "count": len(detections)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Instance globale préchargée
yolo_model = YOLOModel().load_model()

def predict_image(image_path: str) -> Dict:
    """Fonction simplifiée pour l'API"""
    return yolo_model.predict(image_path)
