const express = require('express');
const proxyController = require("../controllers/proxy");

const router = express.Router();

router.all('/:domain/*', proxyController.mim);

module.exports = router;