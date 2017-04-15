#!/usr/bin/node
'use strict';

// usage: ./starter.js <port> <fid>
// comment: it takes around 0.1 seconds to start up

const CACHE_FOLDER = './cached-user-function/';
const express = require('express');
if(process.argv.length != 4) {
    console.log('Wrong parameter');
}

// get port
const port = parseInt(process.argv[2]);
if(port == NaN) {
    console.log('Wrong parameter');
}

// heartbeat
const app = express();
app.get('/heartbeat', function (req, res) {
    res.send('alive\n');
});

// load user code
const uf = process.argv[3]; 
console.log("===== User Function ======");
console.log(uf);
console.log("== User Function : End ===");
eval(uf);
app.get('/', f);

app.listen(port);
console.log('Running function on http://localhost:' + port);
