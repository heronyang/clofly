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
var fs = require('fs-extra');
var ufTempFile = '/tmp/user-function.js';
try {
	fs.copySync(ufFile, ufTempFile);
	console.log('User function code copied locally.');
} catch (err) {
	console.error(err)
}

// generate fid
var crypto = require('crypto');
var fid = crypto.randomBytes(8).toString('hex');

// compress
var AdmZip = require('adm-zip');
var zip = new AdmZip();
zip.addLocalFile(ufTempFile);
for(var f of extraFiles) {
    zip.addLocalFile(f);
}
var zipFile = '/tmp/' + fid + '.zip';
zip.writeZip(zipFile);

console.log('fid = ' + fid);

// upload
var params = {
	localFile: zipFile,

	s3Params: {
		Bucket: 'clofly',
		Key: 'uf-' + fid,
	},
};

var uploader = client.uploadFile(params);
uploader.on('error', function(err) {
	console.error("unable to upload:", err.stack);
});
uploader.on('progress', function() {
	console.log("progress", uploader.progressMd5Amount,
			uploader.progressAmount, uploader.progressTotal);
});
uploader.on('end', function() {
	console.log("done uploading");

	// remove temp file
	fs.unlinkSync(zipFile);

	console.log('Done.');
});

