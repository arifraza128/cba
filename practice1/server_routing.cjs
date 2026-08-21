const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/') {
    res.end("Home Page");
  } else if (req.url === '/about') {
    res.end("This is the about page");
  } else if (req.url === '/products') {
    res.end("This is the products page");
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end("Page not found");
  }
});

const PORT = 5000;
server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
