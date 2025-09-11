const { formatError } = require('../utils/responseFormatter');

const errorHandler = (err, req, res, next) => {
  console.error('Error:', err);

  // Default error response
  let statusCode = 500;
  let message = 'Internal server error';

  // Handle specific error types
  if (err.name === 'ValidationError') {
    statusCode = 400;
    message = 'Validation error';
  } else if (err.message) {
    message = err.message;
  }

  res.status(statusCode).json(formatError(message, statusCode));
};

module.exports = errorHandler;