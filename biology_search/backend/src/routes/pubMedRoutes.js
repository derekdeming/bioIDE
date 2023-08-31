const express = require('express');
const router = express.Router();
const pubMedController = require('../controllers/pubMedController');

router.get('/esearch', pubMedController.eSearch);
router.get('/esummary', pubMedController.eSummary);
router.get('/efetch', pubMedController.eFetch);
router.get('/epost', pubMedController.ePost);
router.get('/elink', pubMedController.eLink);

module.exports = router;
