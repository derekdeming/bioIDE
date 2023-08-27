import React from 'react';

const Results = ({ data }) => {
  return (
    <div>
      {data.map((item, index) => <p key={index}>{item}</p>)}
    </div>
  );
}

export default Results;
