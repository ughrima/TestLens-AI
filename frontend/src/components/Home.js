import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';  

const Home = () => {
  return (
    <div className="home-container">
      <h1>Transform Your Testing Experience with Our Smart Generator</h1>
      <Link to="/upload-images">
        <button className="start-button">Start Generating Testing Instructions</button>
      </Link>
    </div>
  );
};

export default Home;
