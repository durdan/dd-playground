const express = require('express');
const router = express.Router();
const { createBookValidation, updateBookValidation } = require('../validators/bookValidators');
const { handleValidationErrors } = require('../middleware/validationMiddleware');

// Mock book storage (replace with actual database)
let books = [];
let nextId = 1;

// Create a new book
router.post('/', 
  createBookValidation,
  handleValidationErrors,
  (req, res) => {
    const { title, author, isbn, publishedYear, genre } = req.body;
    
    const newBook = {
      id: nextId++,
      title,
      author,
      isbn: isbn.replace(/[-\s]/g, ''), // Store clean ISBN
      publishedYear,
      genre: genre || null,
      createdAt: new Date().toISOString()
    };
    
    books.push(newBook);
    
    res.status(201).json({
      success: true,
      message: 'Book created successfully',
      data: newBook
    });
  }
);

// Update a book
router.put('/:id',
  updateBookValidation,
  handleValidationErrors,
  (req, res) => {
    const bookId = parseInt(req.params.id);
    const bookIndex = books.findIndex(book => book.id === bookId);
    
    if (bookIndex === -1) {
      return res.status(404).json({
        success: false,
        message: 'Book not found'
      });
    }
    
    const updates = req.body;
    if (updates.isbn) {
      updates.isbn = updates.isbn.replace(/[-\s]/g, ''); // Clean ISBN
    }
    
    books[bookIndex] = { ...books[bookIndex], ...updates };
    
    res.json({
      success: true,
      message: 'Book updated successfully',
      data: books[bookIndex]
    });
  }
);

// Get all books
router.get('/', (req, res) => {
  res.json({
    success: true,
    data: books
  });
});

module.exports = router;