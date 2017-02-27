#!/usr/bin/env node
'use strict';

var fs = require('fs');
var config = require('./config.json');

function getFunctionFilename() {
    // get filename
    var argv = process.argv.slice(2);
    if(argv.length != 1) {
        console.error('Invalide filename input');
        process.exit();
    }

    // read the file
    var filename = argv[0];
    return filename;
}

function readFunctionFromFile(filename) {
    return fs.readFileSync(filename, 'utf8');
}

function uploadFunction(functionCode) {

    var AWS = require("aws-sdk");
    AWS.config.update({ region: "us-east-1" });
    var dbClient = new AWS.DynamoDB.DocumentClient();

    var crypto = require('crypto');
    var fid = crypto.randomBytes(config.FID_LENGTH).toString('hex');
    var userFunction = {
        'fid': fid,
        'code': functionCode
    };
	var params = {
		TableName: config.DB_TABLE_NAME,
		Item: userFunction,
	};

	dbClient.put(params, function(err, data) {
		if(err) {
			// error
			console.log("Error: ", JSON.stringify(err, null, 2));
			return;
		}
		// success
        console.log('Okay, deployed URL: ' + config.URL_PREFIX + fid);
	});

}

// main
if (require.main === module) {
    var filename = getFunctionFilename();
    var f = readFunctionFromFile(filename);
    uploadFunction(f);
}
