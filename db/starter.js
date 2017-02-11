/*
 * Connection setups
 */
var mongoose = require('mongoose');

const MONGODB_URI = 'mongodb://localhost/dasf';

mongoose.Promise = global.Promise;
mongoose.connect(MONGODB_URI);

mongoose.connection.on('connected', function () {
    console.log('Mongoose is connected to ' + MONGODB_URI);
});
mongoose.connection.on('error',function (err) {
    console.log('Mongoose has error: ' + err);
});
mongoose.connection.on('disconnected', function () {
    console.log('Mongoose is disconnected');
});

var models = require('./models')(mongoose);

/*
 * Remove previous collections
 */
models.UserFunction.remove({}, function(err) {
    console.log('previous UserFunction collection removed');
});

/*
 * Create a hello function for testing
 */
var helloFunction = new models.UserFunction({
    code: 'console.log("hello");'
});

helloFunction.save(function(err) {

    if(err) {
        res.json({"message": errorMsg});
        console.log(logPrefix + 'db insertion error');
        return;
    }

    // success
    console.log("Hello Function is added");
    mongoose.connection.close(function() {
        console.log('Database disconnected.');
        process.exit(0);
    });

});
