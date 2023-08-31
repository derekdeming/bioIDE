// pubMedController.js
const axios = require('axios');
const base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';

exports.eSearch = async (req, res) => {
  const { query } = req.params;
  const url = `${base}esearch.fcgi?db=pubmed&term=${query}&usehistory=y&retmode=json`;

  try {
    const response = await axios.get(url);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'An error occurred' });
  }
};
