'use strict';

const express = require('express');

// Constants
const PORT = 8080;

// App
const app = express();
app.get('/heartbeat', function (req, res) {
  res.send('alive\n');
});

app.listen(PORT);
console.log('Running on http://localhost:' + PORT);
