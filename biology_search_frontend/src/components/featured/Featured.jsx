import React from "react";
import "./Featured.scss";

function Featured() {
  return (
    <div className="featured">
      <div className="container">
        <div className="left">
          <h1>
            Query and Filter <span>Databases</span> for your Research
          </h1>
          <div className="search">
            <div className="searchInput">
              <img src="./img/search.png" alt="" />
              <input type="text" placeholder='Try "Structural analysis of mutated p450 proteins"' />
            </div>
            <button>Search</button>
          </div>
          <div className="popular">
            <span>Popular:</span>
            <button>Protein Engineering</button>
            <button>RNAseq</button>
            <button>Small Molecule</button>
            <button>AI Services</button>
          </div>
        </div>
        <div className="right">
          <img src="" alt="" />
        </div>
      </div>
    </div>
  );
}

export default Featured;