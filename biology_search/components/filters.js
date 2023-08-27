// components/Filters.js

import React from 'react';
import PropTypes from 'prop-types';

const Filters = ({ onFilter }) => {
  return (
    <div>
      <button onClick={() => onFilter('Filter 1')}>Filter 1</button>
      <button onClick={() => onFilter('Filter 2')}>Filter 2</button>
    </div>
  );
};

Filters.propTypes = {
  onFilter: PropTypes.func.isRequired,
};

export default Filters;
