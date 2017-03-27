global.f = function (req, res) {
	var weather = require('weather-js');
	weather.find({search: 'Pittsburgh, PA', degreeType: 'C'}, function(err, result) {
		if(err) console.log(err);
		res.send(JSON.stringify(result, null, 2));
	});
}
