#!/usr/bin/env node
'use strict';

// setup s3
var s3 = require('s3');
var config = require('./config.json');
var client = s3.createClient({
	s3Options: {
		accessKeyId: config.AWS_ACCESS_KEY_ID,
		secretAccessKey: config.AWS_SECRET_ACCESS_KEY,
	},
});

// read input filename
var argv = process.argv.slice(2);
if(argv.length < 1) {
    console.error('Invalide filename input');
    process.exit();
}

var ufFile = "";
var extraFiles = [];
for(var v of argv) {
    if(ufFile == "") {
        ufFile = v;
    } else {
        extraFiles.push(v);
    }
}

console.log('User Function File: ', ufFile);
console.log('Other Files: ', extraFiles);

// rename user function file
var fs = require('fs-extra')
var ufTempFile = '/tmp/user-function.js';
fs.copy(ufFile, ufTempFile, function(err) {
    if(err) {
        return console.error(err);
    }
    console.log('User function code copied locally.');
});

// generate fid
var crypto = require('crypto');
var fid = crypto.randomBytes(20).toString('hex');

// compress
var AdmZip = require('adm-zip');
var zip = new AdmZip();
zip.addLocalFile(ufTempFile);
for(var f in extraFiles) {
    zip.addLocalFile(f);
}
zip.writeZip('/tmp/' + fid + '.zip');

console.log('fid = ' + fid);
