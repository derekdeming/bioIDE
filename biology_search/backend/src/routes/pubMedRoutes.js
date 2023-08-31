const express = require('express');
const axios = require('axios');
const xml2js = require('xml2js');

const router = express.Router();

router.get('/api/getPubMedData/:query', async (req, res) => {
  const { query } = req.params;
  const pubMedUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${query}&usehistory=y`;

  try {
    const response = await axios.get(pubMedUrl);
    xml2js.parseString(response.data, (err, result) => {
      if (err) {
        return res.status(500).json({ error: 'Error parsing XML data' });
      }
      res.json(result); // Now the data is a JS object
    });
  } catch (error) {
    res.status(500).json({ error: 'An error occurred' });
  }
});

module.exports = router;
