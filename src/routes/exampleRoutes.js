const express = require('express');
const asyncHandler = require('../utils/asyncHandler');
const { 
  ValidationError, 
  NotFoundError, 
  UnauthorizedError,
  ConflictError 
} = require('../errors/ErrorTypes');

const router = express.Router();

// Success case
router.get('/success', (req, res) => {
  res.json({ success: true, data: { message: 'Everything works!' } });
});

// Validation error example
router.post('/validate', (req, res, next) => {
  const { email, age } = req.body;
  const errors = [];

  if (!email || !email.includes('@')) {
    errors.push({ field: 'email', message: 'Valid email is required' });
  }

  if (!age || age < 18) {
    errors.push({ field: 'age', message: 'Age must be 18 or older' });
  }

  if (errors.length > 0) {
    const error = new ValidationError('Validation failed');
    error.details = errors;
    return next(error);
  }

  res.json({ success: true, data: { message: 'Validation passed' } });
});

// Not found error example
router.get('/user/:id', asyncHandler(async (req, res, next) => {
  const { id } = req.params;
  
  // Simulate database lookup
  if (id !== '123') {
    throw new NotFoundError('User');
  }

  res.json({ success: true, data: { id, name: 'John Doe' } });
}));

// Unauthorized error example
router.get('/protected', (req, res, next) => {
  const token = req.headers.authorization;
  
  if (!token) {
    return next(new UnauthorizedError('Token required'));
  }

  res.json({ success: true, data: { message: 'Access granted' } });
});

// Conflict error example
router.post('/user', (req, res, next) => {
  const { email } = req.body;
  
  // Simulate duplicate email check
  if (email === 'taken@example.com') {
    return next(new ConflictError('Email already exists'));
  }

  res.json({ success: true, data: { message: 'User created' } });
});

// Async error example
router.get('/async-error', asyncHandler(async (req, res) => {
  // Simulate async operation that fails
  await new Promise((resolve, reject) => {
    setTimeout(() => reject(new Error('Async operation failed')), 100);
  });
}));

// Unhandled error example
router.get('/unhandled', (req, res) => {
  // This will be caught by error middleware
  throw new Error('Unhandled synchronous error');
});

module.exports = router;