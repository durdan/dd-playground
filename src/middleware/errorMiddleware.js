const { AppError } = require('../errors/ErrorTypes');

const formatErrorResponse = (error, includeStack = false) => {
  const response = {
    success: false,
    error: {
      message: error.message,
      code: error.errorCode || 'INTERNAL_ERROR',
      statusCode: error.statusCode || 500
    }
  };

  // Include additional details for validation errors
  if (error.details) {
    response.error.details = error.details;
  }

  // Include stack trace in development
  if (includeStack && error.stack) {
    response.error.stack = error.stack;
  }

  return response;
};

const handleDatabaseError = (error) => {
  // Handle common database errors
  if (error.code === 11000) {
    return new AppError('Duplicate field value', 400, 'DUPLICATE_FIELD');
  }
  
  if (error.name === 'CastError') {
    return new AppError('Invalid ID format', 400, 'INVALID_ID');
  }

  return new AppError('Database operation failed', 500, 'DATABASE_ERROR');
};

const handleJWTError = (error) => {
  if (error.name === 'JsonWebTokenError') {
    return new AppError('Invalid token', 401, 'INVALID_TOKEN');
  }
  
  if (error.name === 'TokenExpiredError') {
    return new AppError('Token expired', 401, 'TOKEN_EXPIRED');
  }

  return error;
};

const errorHandler = (error, req, res, next) => {
  let processedError = error;

  // Handle operational errors (our custom errors)
  if (!(error instanceof AppError)) {
    // Handle specific third-party errors
    if (error.name === 'ValidationError') {
      const details = Object.values(error.errors).map(err => ({
        field: err.path,
        message: err.message
      }));
      processedError = new AppError('Validation failed', 400, 'VALIDATION_ERROR');
      processedError.details = details;
    } else if (error.code || error.name === 'CastError') {
      processedError = handleDatabaseError(error);
    } else if (error.name?.includes('JWT') || error.name?.includes('Token')) {
      processedError = handleJWTError(error);
    } else {
      // Unknown error - don't leak details in production
      processedError = new AppError(
        process.env.NODE_ENV === 'development' ? error.message : 'Something went wrong',
        500,
        'INTERNAL_ERROR'
      );
    }
  }

  // Log error for monitoring
  console.error('Error:', {
    message: processedError.message,
    statusCode: processedError.statusCode,
    errorCode: processedError.errorCode,
    stack: error.stack,
    url: req.originalUrl,
    method: req.method,
    ip: req.ip,
    userAgent: req.get('User-Agent')
  });

  // Send error response
  const includeStack = process.env.NODE_ENV === 'development';
  const errorResponse = formatErrorResponse(processedError, includeStack);
  
  res.status(processedError.statusCode).json(errorResponse);
};

// Handle unhandled routes
const notFoundHandler = (req, res, next) => {
  const error = new AppError(
    `Route ${req.originalUrl} not found`,
    404,
    'ROUTE_NOT_FOUND'
  );
  next(error);
};

module.exports = {
  errorHandler,
  notFoundHandler,
  formatErrorResponse
};