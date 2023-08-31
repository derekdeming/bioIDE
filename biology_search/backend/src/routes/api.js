const express = require('express');
const router = express.Router();
const fetchController = require('../controllers/fetchController');

router.get('/fetchData', fetchController.fetchData);

module.exports = router;
