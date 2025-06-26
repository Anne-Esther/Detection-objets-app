from flask import Flask, render_template, request, jsonify
import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import warnings

# Configuration de l'application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ignorer les avertissements spécifiques
warnings.filterwarnings("ignore", message="`resume_download` is deprecated")

# Initialisation du modèle
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

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
            # Traitement de l'image
            image = Image.open(file.stream).convert('RGB')
            
            # Redimensionnement (Bonus 3)
            image = image.resize((384, 384))
            
            # Génération de la description avec padding
            inputs = processor(image, return_tensors="pt", padding=True)
            out = model.generate(**inputs)
            description = processor.decode(out[0], skip_special_tokens=True)
            
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
