const express = require('express');
const cors = require('cors');

const proxy = require('./routes/proxy');

const app = express();
app.use(cors());

app.set('trust proxy', true);
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

/* Routes used */
app.use('/proxy', proxy);

app.use((req, res, next) => { res.status(404).json({ message: 'Endpoint not found' }) });

module.exports = app;