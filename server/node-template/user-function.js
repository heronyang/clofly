global.f = function (req, res) {
    res.send('Hello World, ' + today());
}

function today() {
    return new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '');
}
