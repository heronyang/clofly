'use strict';

const express = require('express');

// Constants
const PORT = 8080;

// App
const app = express();
app.get('/test', function (req, res) {
  res.send('Alive\n');
});

app.listen(PORT);
console.log('Running on http://localhost:' + PORT);
