const express = require('express');
const axios = require('axios');
const app = express();
const port = 3001; 

app.get('/searchPubmed', async (req, res) => {
  const { query } = req.query;
  const pubMedUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${query}&usehistory=y&retmode=json`;

  try {
    const response = await axios.get(pubMedUrl);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'An error occurred' });
  }
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
