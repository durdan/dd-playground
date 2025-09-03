const request = require('supertest');
const app = require('../server');

describe('Server endpoints', () => {
  test('GET /health should return healthy status', async () => {
    const response = await request(app)
      .get('/health')
      .expect(200);
    
    expect(response.body).toHaveProperty('status', 'healthy');
    expect(response.body).toHaveProperty('timestamp');
  });

  test('GET /api/users should return users data', async () => {
    const response = await request(app)
      .get('/api/users')
      .expect('Content-Type', /json/);
    
    expect(response.body).toHaveProperty('message');
  });

  test('GET /nonexistent should return 404', async () => {
    await request(app)
      .get('/nonexistent')
      .expect(404);
  });
});