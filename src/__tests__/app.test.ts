import request from 'supertest';
import { app } from '../index';

describe('App', () => {
  it('should return 404 for unknown routes', async () => {
    const response = await request(app)
      .get('/unknown-route')
      .expect(404);

    expect(response.body).toHaveProperty('error', 'Route not found');
  });

  it('should handle JSON parsing errors', async () => {
    const response = await request(app)
      .post('/health')
      .send('invalid json')
      .set('Content-Type', 'application/json')
      .expect(400);
  });
});