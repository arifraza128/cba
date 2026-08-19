const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

const app = express();
app.use(cors());
app.use(express.json());

const SECRET_KEY = 'mysecretkey'; // move to .env in real projects

// Mock database user - store the password as a bcrypt hash
// 'hari123' hashed with bcrypt:
const HASHED_PASSWORD = bcrypt.hashSync('hari123', 10);

const USER = {
  id: 1,
  email: 'hari@gmail.com',
  password: HASHED_PASSWORD, // hashed password stored in "database"
  username: 'hari'
};

// Login Route (POST /)
app.post('/', async (req, res) => {
  const { email, password } = req.body;
  
  if (email === USER.email) {
    try {
      // Verify password using bcrypt
      const isMatch = await bcrypt.compare(password, USER.password);
      if (isMatch) {
        const token = jwt.sign(
          { id: USER.id, email: USER.email, username: USER.username },
          SECRET_KEY,
          { expiresIn: '1h' }
        );
        return res.json({ token });
      }
    } catch (err) {
      return res.status(500).json({ message: 'Internal server error during authentication' });
    }
  }
  
  res.status(401).json({ message: 'Invalid User' });
});

// Protected Profile Route (GET /profile)
app.get('/profile', verifyToken, (req, res) => {
  res.json({
    message: 'Welcome to the protected profile route!',
    user: req.user
  });
});

// Verify route with bcrypt (POST /verify)
// Demonstrates bcrypt comparison directly
app.post('/verify', async (req, res) => {
  const { password, hash } = req.body;
  if (!password || !hash) {
    return res.status(400).json({ message: 'Both password and hash are required in body' });
  }
  try {
    const isMatch = await bcrypt.compare(password, hash);
    res.json({ isMatch });
  } catch (err) {
    res.status(500).json({ message: 'Bcrypt verification failed', error: err.message });
  }
});

// Middleware to verify JWT token
function verifyToken(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).json({ message: 'Access denied. No token provided.' });
  }
  
  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, SECRET_KEY);
    req.user = decoded;
    next();
  } catch (err) {
    res.status(403).json({ message: 'Token expired or invalid.' });
  }
}

app.listen(5000, () => {
  console.log('Server is running on port 5000');
});
