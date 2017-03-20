global.f = function (req, res) {
    var randomstring = require("randomstring");
    res.send('Hello! Good!! ' + randomstring.generate());
}
