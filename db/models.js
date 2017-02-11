/*
 * Model setups
 */
module.exports = function(mongoose) {

    var Schema = mongoose.Schema;

    var UserFunction = new Schema({
        version: Number,
        code: {type: String, required: true}
    });

	var models = {
		UserFunction: mongoose.model('UserFunctions', UserFunction),
	};

	return models;

};
