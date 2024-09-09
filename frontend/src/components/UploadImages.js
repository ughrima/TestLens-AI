import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

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

    // Append images and context
    images.forEach((image) => {
      formData.append('images', image);
    });
    formData.append('context', context);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/describe', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to fetch instructions');
      }

      const result = await response.json();
      navigate('/result', { state: { instructions: JSON.stringify(result.instructions, null, 2) } });
    } catch (error) {
      console.error('Error generating instructions:', error);
      alert('Failed to generate instructions. Please try again.');
    }
  };

  return (
    <div>
      <h2>Upload Screenshots and Provide Context</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Context (optional):</label>
          <textarea value={context} onChange={(e) => setContext(e.target.value)} />
        </div>
        <div>
          <label>Upload Screenshots:</label>
          <input type="file" multiple accept="image/*" onChange={handleImageChange} />
        </div>
        <button type="submit">Describe Testing Instructions</button>
      </form>
    </div>
  );
};

export default UploadImages;
