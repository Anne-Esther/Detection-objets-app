@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'Aucune image fournie'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Aucune image sélectionnée'}), 400
        
    if file and allowed_file(file.filename):
        try:
            # 1. Chargement de l'image
            image = Image.open(file.stream).convert('RGB')
            
            # 2. Pré-traitement renforcé
            inputs = processor(
                images=image, 
                return_tensors="pt",
                padding="max_length",  # Padding maximal
                max_length=77,        # Taille fixe pour BLIP
                truncation=True,
                return_attention_mask=True
            )
            
            # 3. Génération avec paramètres optimisés
            outputs = model.generate(
                **inputs,
                max_new_tokens=50,
                num_beams=4,
                early_stopping=True
            )
            
            description = processor.decode(outputs[0], skip_special_tokens=True)
            return jsonify({'description': description})
            
        except Exception as e:
            return jsonify({'error': f"Erreur technique: {str(e)}"}), 500
