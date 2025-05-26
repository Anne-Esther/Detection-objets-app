from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import predict
import os
import uvicorn

# Configuration de l'application
app = FastAPI(
    title="API de Détection d'Objets",
    description="API utilisant YOLOv5 pour la détection d'objets",
    version="1.0.0"
)

# CORS settings (à adapter pour la production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À remplacer par vos URLs frontend en production
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Include routes
app.include_router(
    predict.router,
    prefix="/api/v1",  # Ajout d'un préfixe pour la versioning
    tags=["Prédictions"]
)

# Configuration pour le lancement direct
if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8000)),
        reload=False,  # Désactivé en production
        workers=1,    # Adapté pour les hébergements avec ressources limitées
        log_level="info"
    )
