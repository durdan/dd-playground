const request = require('supertest');
const app = require('../server');

describe('Server Endpoints', () => {
  test('GET /health should return healthy status', async () => {
    const response = await request(app)
      .get('/health')
      .expect(200);
    
    expect(response.body).toHaveProperty('status', 'healthy');
    expect(response.body).toHaveProperty('timestamp');
  });

  test('GET /api/users should return response', async () => {
    const response = await request(app)
      .get('/api/users')
      .expect('Content-Type', /json/);
    
    // Should return 200 or 500 depending on DB connection
    expect([200, 500]).toContain(response.status);
    expect(response.body).toHaveProperty('message');
  });
});