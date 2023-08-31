const express = require('express');
const app = express();
const port = 3001;

// Import routes
const apiRoutes = require('./src/routes/api');

app.use(express.json());

// Use imported routes
app.use('/api', apiRoutes);

app.listen(port, () => {
  console.log(`Backend server running at http://localhost:${port}`);
});
