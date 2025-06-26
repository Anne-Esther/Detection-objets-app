from flask import Flask, render_template, request, jsonify
import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import warnings

# Configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Ignorer les avertissements
warnings.filterwarnings("ignore", message="`resume_download` is deprecated")

# Modèle BLIP
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
        return jsonify({'error': 'No image provided'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
        
    try:
        # Traitement optimisé pour PyTorch 2.7.1
        image = Image.open(file.stream).convert('RGB')
        image = image.resize((384, 384))  # Taille standard pour BLIP
        
        # Configuration améliorée du padding
        inputs = processor(
            text=None,
            images=image,
            return_tensors="pt",
            padding="max_length",
            max_length=77,
            truncation=True
        )
        
        # Génération avec paramètres optimisés
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,
            num_beams=4,
            early_stopping=True
        )
        
        description = processor.decode(outputs[0], skip_special_tokens=True)
        return jsonify({'description': description})
        
    except Exception as e:
        return jsonify({'error': f"Processing error: {str(e)}"}), 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5000)
