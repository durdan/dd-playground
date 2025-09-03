const { body, validationResult } = require('express-validator');

// Validation rules for book creation
const createBookValidation = [
  body('title')
    .trim()
    .notEmpty()
    .withMessage('Title is required')
    .isLength({ min: 1, max: 200 })
    .withMessage('Title must be between 1 and 200 characters'),

  body('author')
    .trim()
    .notEmpty()
    .withMessage('Author is required')
    .isLength({ min: 1, max: 100 })
    .withMessage('Author must be between 1 and 100 characters'),

  body('isbn')
    .trim()
    .notEmpty()
    .withMessage('ISBN is required')
    .custom((value) => {
      // Remove hyphens and spaces for validation
      const cleanISBN = value.replace(/[-\s]/g, '');
      const isValidISBN10 = /^\d{9}[\dX]$/.test(cleanISBN);
      const isValidISBN13 = /^\d{13}$/.test(cleanISBN);
      
      if (!isValidISBN10 && !isValidISBN13) {
        throw new Error('Invalid ISBN format');
      }
      return true;
    }),

  body('publishedYear')
    .isInt({ min: 1000, max: new Date().getFullYear() })
    .withMessage(`Published year must be between 1000 and ${new Date().getFullYear()}`),

  body('genre')
    .optional()
    .trim()
    .isLength({ max: 50 })
    .withMessage('Genre must not exceed 50 characters')
];

// Validation rules for book updates (all fields optional)
const updateBookValidation = [
  body('title')
    .optional()
    .trim()
    .notEmpty()
    .withMessage('Title cannot be empty')
    .isLength({ min: 1, max: 200 })
    .withMessage('Title must be between 1 and 200 characters'),

  body('author')
    .optional()
    .trim()
    .notEmpty()
    .withMessage('Author cannot be empty')
    .isLength({ min: 1, max: 100 })
    .withMessage('Author must be between 1 and 100 characters'),

  body('isbn')
    .optional()
    .trim()
    .notEmpty()
    .withMessage('ISBN cannot be empty')
    .custom((value) => {
      const cleanISBN = value.replace(/[-\s]/g, '');
      const isValidISBN10 = /^\d{9}[\dX]$/.test(cleanISBN);
      const isValidISBN13 = /^\d{13}$/.test(cleanISBN);
      
      if (!isValidISBN10 && !isValidISBN13) {
        throw new Error('Invalid ISBN format');
      }
      return true;
    }),

  body('publishedYear')
    .optional()
    .isInt({ min: 1000, max: new Date().getFullYear() })
    .withMessage(`Published year must be between 1000 and ${new Date().getFullYear()}`),

  body('genre')
    .optional()
    .trim()
    .isLength({ max: 50 })
    .withMessage('Genre must not exceed 50 characters')
];

module.exports = {
  createBookValidation,
  updateBookValidation
};