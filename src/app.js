const express = require('express');
const { requestLogger } = require('./middleware/logging');
const userRoutes = require('./routes/users');

const app = express();

app.use(express.json());
app.use(requestLogger);
app.use('/users', userRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

module.exports = app;