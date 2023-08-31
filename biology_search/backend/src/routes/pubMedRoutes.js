// pubmedRoutes.js
const express = require('express');
const router = express.Router();
const pubMedController = require('../controllers/pubMedController');

router.get('/getPubMedData/:query', pubMedController.eSearch);

module.exports = router;
