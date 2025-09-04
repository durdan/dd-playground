import request from 'supertest';
import express from 'express';
import { errorHandler, AppError } from '../errorHandler';

const createTestApp = () => {
  const app = express();
  
  app.get('/test-error', (req, res, next) => {
    const error: AppError = new Error('Test error');
    error.statusCode = 400;
    next(error);
  });
  
  app.get('/test-default-error', (req, res, next) => {
    next(new Error('Default error'));
  });
  
  app.use(errorHandler);
  return app;
};

describe('Error Handler', () => {
  const app = createTestApp();

  it('should handle custom error with status code', async () => {
    const response = await request(app)
      .get('/test-error')
      .expect(400);

    expect(response.body.error.message).toBe('Test error');
    expect(response.body.error.status).toBe(400);
  });

  it('should handle default error with 500 status', async () => {
    const response = await request(app)
      .get('/test-default-error')
      .expect(500);

    expect(response.body.error.message).toBe('Default error');
    expect(response.body.error.status).toBe(500);
  });
});