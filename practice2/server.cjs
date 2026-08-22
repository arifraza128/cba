const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
  if (req.method === 'GET' && req.url === '/') {
    const filePath = path.join(__dirname, 'form.html');
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Error loading form.html');
        return;
      }
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(data);
    });
  } else if (req.method === 'POST' && req.url === '/submit') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      // Process the form data
      const formData = new URLSearchParams(body);
      const name = formData.get('name');
      const email = formData.get('email');
      const course = formData.get('course');
      const age = formData.get('age');

      const responseMessage = `
Name: ${name}
Email: ${email}
Course: ${course}
Age: ${age}
--------------------------------------------------\n`;

      // Save to data.txt in the same directory
      const dataPath = path.join(__dirname, 'data.txt');
      fs.appendFile(dataPath, responseMessage, (err) => {
        if (err) {
          res.writeHead(500, { 'Content-Type': 'text/plain' });
          res.end('Error saving data');
          return;
        }
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(`
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Registration Successful</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #74ebd5, #9face6);
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      margin: 0;
    }
    .success-container {
      background-color: white;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
      width: 100%;
      max-width: 400px;
      text-align: center;
    }
    h1 {
      color: #2ecc71;
      font-size: 24px;
      margin-top: 0;
    }
    p {
      color: #555;
      font-size: 16px;
      margin: 8px 0;
    }
    .details {
      text-align: left;
      background-color: #f9f9f9;
      padding: 15px;
      border-radius: 8px;
      margin: 20px 0;
      border-left: 4px solid #2ecc71;
    }
    a {
      display: inline-block;
      margin-top: 15px;
      color: #6c5ce7;
      text-decoration: none;
      font-weight: bold;
      transition: color 0.3s;
    }
    a:hover {
      color: #5b4bc4;
    }
  </style>
</head>
<body>
  <div class="success-container">
    <h1>Registration Successful</h1>
    <p>Thank you for registering!</p>
    <div class="details">
      <p><b>Name:</b> ${name}</p>
      <p><b>Email:</b> ${email}</p>
      <p><b>Course:</b> ${course}</p>
      <p><b>Age:</b> ${age}</p>
    </div>
    <a href="/">Go back to the form</a>
  </div>
</body>
</html>
        `);
      });
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'text/html' });
    res.end(`
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>404 Not Found</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      text-align: center;
      padding: 50px;
      background-color: #f4f4f9;
    }
    h1 { color: #e74c3c; }
  </style>
</head>
<body>
  <h1>404 Not Found</h1>
  <p>The page you requested could not be found.</p>
  <a href="/">Go back to Home</a>
</body>
</html>
    `);
  }
});

const PORT = 5000;
server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
