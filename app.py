from flask import Flask, render_template, request, jsonify
import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from transformers import logging

# Désactive les avertissements inutiles
logging.set_verbosity_error()

# Configuration Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Initialisation BLIP avec paramètres optimisés
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base",
    use_fast=False  # Désactive explicitement le processeur rapide
)
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'Aucune image fournie'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Aucune image sélectionnée'}), 400
        
    if file and allowed_file(file.filename):
        try:
            # 1. Chargement et redimensionnement
            image = Image.open(file.stream).convert('RGB')
            image = image.resize((384, 384))  # Taille fixe
            
            # 2. Pré-traitement avec padding renforcé
            inputs = processor(
                images=image,
                return_tensors="pt",
                padding="max_length",  # Padding maximal
                max_length=77,        # Standard BLIP
                truncation=True,
                return_attention_mask=True
            )
            
            # 3. Génération avec paramètres optimisés
            outputs = model.generate(
                **inputs,
                max_new_tokens=50,    # Longueur de description
                num_beams=4,          # Qualité améliorée
                early_stopping=True
            )
            
            description = processor.decode(outputs[0], skip_special_tokens=True)
            return jsonify({
                'success': True,
                'description': description
            })
            
        except Exception as e:
            return jsonify({
                'error': f"Erreur de traitement: {str(e)}"
            }), 500
            
    return jsonify({'error': 'Type de fichier non autorisé'}), 400

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
