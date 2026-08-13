import express from 'express';
import cors from 'cors';

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

app.post('/api/users', (req, res) => {
  const { name, email, age } = req.body;

  if (!name || !email || !age) {
    return res.status(400).json({
      success: false,
      message: 'Name, email and age required',
    });
  }

  const user = {
    id: Date.now(),
    name,
    email,
    age,
  };

  console.log('received user:', user);

  res.status(201).json({
    success: true,
    message: 'User created successfully',
    data: user,
  });
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
