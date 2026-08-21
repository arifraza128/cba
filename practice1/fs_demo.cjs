const fs = require('fs');
const path = require('path');

// Target file path inside the practice directory
const filePath = path.join(__dirname, 'a1.txt');

console.log('--- Writing to file ---');
fs.writeFileSync(filePath, "This is just one line content to be written in the file");
console.log('Written to a1.txt successfully.');

console.log('\n--- Reading from file ---');
const text = fs.readFileSync(filePath, "utf8");
console.log('Content:\n' + text);

console.log('\n--- Appending to file ---');
fs.appendFileSync(filePath, "\nThis is the second line content to be appended in the file");
console.log('Appended successfully.');

console.log('\n--- Reading updated file ---');
const updatedText = fs.readFileSync(filePath, "utf8");
console.log('Updated Content:\n' + updatedText);
