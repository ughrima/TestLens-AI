import React from 'react';
import { useLocation } from 'react-router-dom';
import './ResultPage.css'; 

const ResultPage = () => {
  const location = useLocation();
  const { instructions } = location.state || { instructions: "No instructions generated." };

  return (
    <div className="result-container">
      <h2>Testing Instructions</h2>
      <pre className="instructions-text">{instructions}</pre>
    </div>
  );
};

export default ResultPage;
