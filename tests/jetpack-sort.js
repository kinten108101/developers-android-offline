const readline = require('readline');
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

const lines = [];

rl.on('line', function(line){
	lines.push(line);
});

rl.on('close', function() {
	lines
		.sort()
		.reverse()
		.forEach(z => process.stdout.write(` ${z}`));
});

