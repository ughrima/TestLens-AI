import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "./UploadImages.css";

const UploadImages = () => {
  const [images, setImages] = useState([]);
  const [context, setContext] = useState('');
  const navigate = useNavigate();

  const handleImageChange = (e) => {
    setImages([...e.target.files]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();

    images.forEach((image) => {
      console.log("Appending file:", image); 
      formData.append('images', image);
    });
    formData.append('context', context);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/describe', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();
      navigate('/result', { state: { instructions: JSON.stringify(result.instructions, null, 2) } });
    } catch (error) {
      console.error('Error generating instructions:', error);
      alert('Error generating instructions. Please try again.');
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Content</h2>
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="form-group">
          <label htmlFor="context">Context (optional):</label>
          <textarea
            id="context"
            className="context-input"
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="Enter context here (optional)"
          />
        </div>
        <div className="form-group">
          <label htmlFor="file-upload">Upload Screenshots:</label>
          <input
            id="file-upload"
            type="file"
            multiple
            accept="image/*"
            className="file-input"
            onChange={handleImageChange}
          />
        </div>
        <button type="submit" className="submit-button">Describe Testing Instructions</button>
      </form>
    </div>
  );
};

export default UploadImages;
