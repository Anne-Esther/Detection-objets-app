from flask import Flask, request, render_template
from transformers import pipeline
import os

app = Flask(__name__)

# Charge un modèle plus simple au démarrage
try:
    detector = pipeline("object-detection", model="facebook/detr-resnet-50")
except Exception as e:
    print(f"Erreur de chargement du modèle: {e}")
    detector = None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            return "Aucun fichier uploadé"
        
        file = request.files['file']
        if file.filename == '':
            return "Aucun fichier sélectionné"
        
        try:
            # Sauvegarde temporaire
            img_path = "temp.jpg"
            file.save(img_path)
            
            if detector:
                results = detector(img_path)
                os.remove(img_path)  # Nettoie
                return render_template("results.html", results=results)
            else:
                return "Modèle non chargé"
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
