'use strict';

const express = require('express');

// Constants
const PORT = 8080;

// App
const app = express();
app.get('/heartbeat', function (req, res) {
  res.send('alive\n');
});

// include user code
var fs = require('fs');
eval(fs.readFileSync('user-function.js')+'');
// var f = require('./user-function.js').f;
app.get('/', f);

app.listen(PORT);
console.log('Running on http://localhost:' + PORT);
