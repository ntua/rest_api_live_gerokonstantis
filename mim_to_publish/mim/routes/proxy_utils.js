const express = require("express");
const proxyUtils = require("../controllers/proxy_utils");

const router = express.Router();

router.get("/export/:domain", proxyUtils.export_calls);

module.exports = router;
