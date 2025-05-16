import axios from 'axios';

// Exemple de fonction pour envoyer une image au backend
async function sendImageToBackend(formData) {
  try {
    const response = await axios.post(
      'https://detectionbackend.onrender.com/api/detect', // URL backend + route API
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    console.log('Réponse backend:', response.data);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la détection:', error);
    throw error;
  }
}
