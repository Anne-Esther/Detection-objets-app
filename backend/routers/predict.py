from fastapi import APIRouter, UploadFile, File, HTTPException
from model.yolo_model import predict_image
import tempfile
import os

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Validation du type de fichier
        if not file.content_type.startswith('image/'):
            raise HTTPException(400, "Seules les images sont acceptées")

        # Sauvegarde temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            content = await file.read()
            if len(content) > 2_000_000:  # 2MB max
                raise HTTPException(413, "Image trop volumineuse")
            temp_file.write(content)
            temp_path = temp_file.name

        # Prédiction
        results = predict_image(temp_path)
        
        # Nettoyage
        os.unlink(temp_path)
        
        return results
    
    except Exception as e:
        raise HTTPException(500, detail=str(e))
