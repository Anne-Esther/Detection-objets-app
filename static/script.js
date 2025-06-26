document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const selectBtn = document.getElementById('selectBtn');
    const resultContainer = document.getElementById('resultContainer');
    const loadingContainer = document.getElementById('loadingContainer');
    const imagePreview = document.getElementById('imagePreview');
    const imageDescription = document.getElementById('imageDescription');
    const newAnalysisBtn = document.getElementById('newAnalysisBtn');

    // Gestion du clic sur le bouton "Parcourir"
    selectBtn.addEventListener('click', () => fileInput.click());

    // Gestion de la sélection de fichier
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length) {
            handleImageUpload(fileInput.files[0]);
        }
    });

    // Gestion du glisser-déposer
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#4285f4';
        uploadArea.style.backgroundColor = 'rgba(66, 133, 244, 0.05)';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#757575';
        uploadArea.style.backgroundColor = 'transparent';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#757575';
        uploadArea.style.backgroundColor = 'transparent';
        
        if (e.dataTransfer.files.length) {
            handleImageUpload(e.dataTransfer.files[0]);
        }
    });

    // Bouton nouvelle analyse
    newAnalysisBtn.addEventListener('click', () => {
        resultContainer.style.display = 'none';
        fileInput.value = '';
    });

    function handleImageUpload(file) {
        // Vérification du type de fichier
        if (!file.type.match('image.*')) {
            alert('Veuillez sélectionner une image valide (JPG, JPEG, PNG)');
            return;
        }

        // Afficher le loader
        loadingContainer.style.display = 'block';
        uploadArea.style.display = 'none';

        // Prévisualisation de l'image
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
        };
        reader.readAsDataURL(file);

        // Envoyer l'image au serveur pour analyse
        const formData = new FormData();
        formData.append('image', file);

        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || 'Erreur serveur'); });
            }
            return response.json();
        })
        .then(data => {
            if (data.error) throw new Error(data.error);
            
            // Afficher les résultats
            imageDescription.textContent = data.description;
            loadingContainer.style.display = 'none';
            resultContainer.style.display = 'flex';
        })
        .catch(error => {
            console.error('Error:', error);
            loadingContainer.style.display = 'none';
            uploadArea.style.display = 'block';
            alert('Erreur: ' + error.message);
        });
    }
});
