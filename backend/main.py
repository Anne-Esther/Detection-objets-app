from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import predict
import os
import uvicorn

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(predict.router)

# Lancement si exécuté directement
if __name__ == '__main__':
    uvicorn.run(
        app, 
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 8000))  # Port par défaut 8000 pour FastAPI
