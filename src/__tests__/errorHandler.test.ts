import { createError } from '../middleware/errorHandler';

describe('Error Handler', () => {
  it('should create error with message and status code', () => {
    const error = createError('Test error', 400);
    
    expect(error.message).toBe('Test error');
    expect(error.statusCode).toBe(400);
    expect(error.isOperational).toBe(true);
  });

  it('should default to status code 500', () => {
    const error = createError('Test error');
    
    expect(error.statusCode).toBe(500);
  });
});