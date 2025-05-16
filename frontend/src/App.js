import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [resultUrl, setResultUrl] = useState(null);

  const handleChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", image);

    const response = await axios.post("http://localhost:8000/upload-image", formData, {
      responseType: "blob",
    });

    const imageBlob = new Blob([response.data], { type: "image/jpeg" });
    const imageUrl = URL.createObjectURL(imageBlob);
    setResultUrl(imageUrl);
  };

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = resultUrl;
    link.download = "image_annotée.jpg";
    link.click();
  };

  return (
    <div className="app">
      <h1 className="title">Détection d’objets</h1>
      <input type="file" onChange={handleChange} />
      <button onClick={handleUpload}>Analyser</button>
      {resultUrl && (
        <div className="result">
          <img src={resultUrl} alt="Résultat" />
          <button onClick={handleDownload}>Télécharger</button>
        </div>
      )}
    </div>
  );
}

export default App;
