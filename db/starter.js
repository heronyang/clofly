var mongoose    = require('mongoose');
var models      = require('./models')(mongoose);
var connect     = require('./connect')(mongoose);

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
    code: "function (req, res) { res.send('hello darf (database init)!!\n'); }"
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
