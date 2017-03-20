console.log('[Start] Install user function depedencies');

var fs = require('fs');

var f = fs.readFileSync('user-function.js', 'utf8');
var re = /require\(.*\)/gi;
var matches = f.match(re);

if(matches == null) {
    console.log('[Done] No user function depedencies found');
    process.exit();
}

var deps = '';
matches.forEach(function(match) {
    var dep = match.substring(9,match.length-2)
    console.log(dep);
    deps += dep + ' ';
});

var command = 'npm install --save ' + deps;
var exec = require('child_process').exec;
exec(command, (error, stdout, stderr) => {
  if (error) {
    console.error(`exec error: ${error}`);
    return;
  }
  console.log(`stdout: ${stdout}`);
  console.log(`stderr: ${stderr}`);
});

console.log('[Done] Install user function depedencies');
