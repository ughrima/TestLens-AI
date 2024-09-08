// import React from 'react';
// import { useLocation } from 'react-router-dom';

// const ResultPage = () => {
//   const location = useLocation();
//   const { instructions } = location.state || { instructions: [] };

//   return (
//     <div>
//       <h2>Testing Instructions</h2>
//       <pre>{instructions}</pre>
//     </div>
//   );
// };

// export default ResultPage;
import React from 'react';
import { useLocation } from 'react-router-dom';

const ResultPage = () => {
  const location = useLocation();
  const { instructions } = location.state || { instructions: [] };

  return (
    <div>
      <h2>Testing Instructions</h2>
      <pre>{instructions}</pre>
    </div>
  );
};

export default ResultPage;
