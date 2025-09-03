const express = require('express');

function createBookRoutes(bookController) {
  const router = express.Router();

  router.post('/books', bookController.createBook);
  router.get('/books', bookController.getAllBooks);
  router.get('/books/:id', bookController.getBookById);
  router.put('/books/:id', bookController.updateBook);
  router.delete('/books/:id', bookController.deleteBook);

  return router;
}

module.exports = createBookRoutes;