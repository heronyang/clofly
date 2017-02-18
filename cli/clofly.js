#!/usr/bin/env node
'use strict';

var URL_PREFIX = 'http://clofly.com/cgi/cgi.py/'
var FID_LENGTH = 8;

// read input filename
var argv = process.argv.slice(2);
if(argv.length != 1) {
    console.error('Invalide filename input');
    process.exit();
}
var filename = argv[0];

// read the input file into buffer
var fs = require('fs');
fs.readFile(filename, 'utf8', function (err, functionCode) {

    // if err
	if(err) {
		return console.log(err);
	}

    // if not, upload to database
    uploadFunctionCode(functionCode);

});

// upload code to database
var AWS = require("aws-sdk");
AWS.config.update({
    region: "us-east-1"
});
var dbClient = new AWS.DynamoDB.DocumentClient();
var userFunctionTable = 'clofly-user-function';

function uploadFunctionCode(functionCode) {

    var crypto = require('crypto');
    var fid = crypto.randomBytes(FID_LENGTH).toString('hex');
    var userFunction = {
        'fid': fid,
        'code': functionCode
    };
	var params = {
		TableName: userFunctionTable,
		Item: userFunction,
	};

	dbClient.put(params, function(err, data) {
		if(err) {
			// error
			console.log("Error: ", JSON.stringify(err, null, 2));
			return;
		}
		// success
        console.log('Done. Deployed URL: ' + URL_PREFIX + fid);
	});

}
