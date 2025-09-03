import { Request, Response, NextFunction } from 'express';
import { errorHandler, createError } from '../errorHandler';

describe('Error Handler', () => {
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;
  let mockNext: NextFunction;

  beforeEach(() => {
    mockRequest = {};
    mockResponse = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn().mockReturnThis()
    };
    mockNext = jest.fn();
  });

  it('should handle custom errors with status code', () => {
    const error = createError('Test error', 400);

    errorHandler(
      error,
      mockRequest as Request,
      mockResponse as Response,
      mockNext
    );

    expect(mockResponse.status).toHaveBeenCalledWith(400);
    expect(mockResponse.json).toHaveBeenCalledWith({
      error: {
        message: 'Test error'
      }
    });
  });

  it('should default to 500 for errors without status code', () => {
    const error = new Error('Generic error');

    errorHandler(
      error,
      mockRequest as Request,
      mockResponse as Response,
      mockNext
    );

    expect(mockResponse.status).toHaveBeenCalledWith(500);
    expect(mockResponse.json).toHaveBeenCalledWith({
      error: {
        message: 'Generic error'
      }
    });
  });

  it('should create error with correct properties', () => {
    const error = createError('Custom error', 404);

    expect(error.message).toBe('Custom error');
    expect(error.statusCode).toBe(404);
    expect(error.isOperational).toBe(true);
  });
});