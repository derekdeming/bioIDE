const express = require('express');
const app = express();
const port = 3001;

// Import routes
const pubMedRoutes = require('./src/routes/pubMedRoutes');

app.use(express.json());

// Use imported routes
app.use('/pubmed', pubMedRoutes);

app.listen(port, () => {
  console.log(`Backend server running at http://localhost:${port}`);
});
