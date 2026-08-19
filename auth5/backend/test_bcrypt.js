const bcrypt = require('bcrypt');

const pwd = 'secret123';
const hash = bcrypt.hashSync(pwd, 10);
console.log('Generated Hash:', hash);

const isMatch = bcrypt.compareSync(pwd, hash);
console.log('Match Sync (Generated Hash):', isMatch);

const externalHash = '$2b$10$wK1F7i9eN4wW2p6g4K.e6eM/7Qx8jNlhFhR.qY2Z1W1S3F4yVpP8q';
const matchExternal = bcrypt.compareSync(pwd, externalHash);
console.log('Match Sync (External Hash):', matchExternal);
