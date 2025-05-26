from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from model.yolo_model import load_model, predict_image

router = APIRouter()

# Charger le modèle une fois au démarrage
model = load_model()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Validation du type de fichier
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Seules les images sont acceptées")
        
        # Sauvegarde temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Prédiction
        results = predict_image(model, temp_path)
        
        # Nettoyage
        os.unlink(temp_path)
        
        if not results.get("success", False):
            raise HTTPException(status_code=500, detail=results.get("error"))
        
        return JSONResponse(content=results)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement: {str(e)}"
        )
