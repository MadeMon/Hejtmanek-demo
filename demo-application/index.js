const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello, World!');
});

const PORT = parseInt(process.env.PORT);
if (PORT !== 80){
  throw new Error(`Invalid port number ${PORT}!`);
}

const server = app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});