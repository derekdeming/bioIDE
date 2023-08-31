const axios = require('axios');
const base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';

exports.eSearch = async (req, res) => {
  try {
    const query = 'asthma[mesh]+AND+leukotrienes[mesh]+AND+2009[pdat]';
    const url = `${base}esearch.fcgi?db=pubmed&term=${query}&usehistory=y`;
    const response = await axios.get(url);
    res.json({ success: true, data: response.data });
  } catch (error) {
    res.json({ success: false, message: 'An error occurred', error });
  }
};

exports.eSummary = async (req, res) => {
  // Similar structure as eSearch
};

exports.eFetch = async (req, res) => {
  // Similar structure as eSearch
};

exports.ePost = async (req, res) => {
  // Similar structure as eSearch
};

exports.eLink = async (req, res) => {
  // Similar structure as eSearch
};
