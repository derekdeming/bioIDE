const express = require('express');
const app = express();
const port = 3001;

// Import routes
const pubMedRoutes = require('./src/routes/pubMedRoutes');

app.use(express.json());
const cors = require('cors');

// Add a default route for the root URL
app.get('/', (req, res) => {
  res.send('Welcome to the PubMed API Server!');
});

// Use imported routes
app.use('/pubmed', pubMedRoutes);
app.use(cors());
app.use((req, res, next) => {
  console.log(`Incoming request: ${req.method} ${req.url}`);
  next();
});

app.listen(port, () => {
  console.log(`Backend server running at http://localhost:${port}`);
});
