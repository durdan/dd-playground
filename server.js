const express = require('express');
const BookStorage = require('./storage/BookStorage');
const BookService = require('./services/BookService');
const BookController = require('./controllers/BookController');
const createBookRoutes = require('./routes/bookRoutes');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Dependencies
const bookStorage = new BookStorage();
const bookService = new BookService(bookStorage);
const bookController = new BookController(bookService);

// Routes
app.use('/api', createBookRoutes(bookController));

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

const server = app.listen(port, () => {
  console.log(`Books API server running on port ${port}`);
});

module.exports = { app, server };