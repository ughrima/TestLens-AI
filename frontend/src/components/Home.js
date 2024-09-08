import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div>
      <h1>Welcome to the Testing Instruction Generator</h1>
      <Link to="/upload-images">
        <button>Start Generating Testing Instructions</button>
      </Link>
    </div>
  );
};

export default Home;
