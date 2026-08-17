const express = require('express');
const cors = require('cors');

const app = express();

app.use(cors());
app.use(express.json());

// Login
app.get('/api/hello', (req, res) => {
  const authHeader = req.headers.authorization;

  // Check authorization header
  if (!authHeader) {
    return res.status(401).send('authorization required');
  }

  // Check Basic auth type
  if (!authHeader.startsWith('Basic ')) {
    return res.status(401).send('Invalid Authentication type');
  }

  // Get base64 encoded credentials
  const encodedCredentials = authHeader.split(' ')[1];

  // Decode base64
  const decodedCredentials = Buffer.from(encodedCredentials, 'base64').toString('utf-8');

  // Split username and password
  const [username, password] = decodedCredentials.split(':');

  console.log('Username', username);
  console.log('Password', password);

  const validUserName = 'admin';
  const validPassword = '2807';

  // Validate credentials
  if (username === validUserName && password === validPassword) {
    return res.send('Welcome! Your AUTHENTICATION successful..');
  }

  return res.status(401).send('invalid username or password');
});

const PORT = 5000;

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});