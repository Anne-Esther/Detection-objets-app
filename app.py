@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
        
    try:
        # Conversion et traitement de l'image
        image = Image.open(file.stream).convert('RGB')
        
        # Modification ici ↓
        inputs = processor(image, return_tensors="pt", padding=True)
        
        out = model.generate(**inputs)
        description = processor.decode(out[0], skip_special_tokens=True)
        return jsonify({'description': description})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
