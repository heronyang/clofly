global.f = function (req, res) {
    res.send('Hi! ' + getName());
}

function getName() {
    return 'Clofly!!';
}
