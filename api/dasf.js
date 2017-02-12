#!/usr/bin/env node
'use strict';

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
var mongoose    = require('mongoose');
var models      = require('../db/models')(mongoose);
var connect     = require('../db/connect')(mongoose);
function uploadFunctionCode(functionCode) {

    var userFunction = new models.UserFunction({
        code: functionCode
    });

    userFunction.save(function(err, uf) {

        if(err) {
            res.json({'message': errorMsg});
            console.log(logPrefix + 'db insertion error');
            return;
        }

        // success
        console.log('\n===========\n');
        console.log('Function URL: http://localhost:8000/cgi/cgi.py/' + uf.id);
        console.log('\n===========\n');
        mongoose.connection.close(function() {
            console.log('Database disconnected.');
            process.exit(0);
        });

    });

}
