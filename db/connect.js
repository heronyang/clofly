/*
 * Connection setups
 */
module.exports = function(mongoose) {

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

}
