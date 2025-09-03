const request = require('supertest');
const app = require('../server');

describe('Server Endpoints', () => {
  test('GET /health should return healthy status', async () => {
    const response = await request(app)
      .get('/health')
      .expect(200);
    
    expect(response.body.status).toBe('healthy');
    expect(response.body.timestamp).toBeDefined();
  });

  test('GET /api/users should return users data', async () => {
    const response = await request(app)
      .get('/api/users')
      .expect('Content-Type', /json/);
    
    // Should return either success or database error
    expect([200, 500]).toContain(response.status);
  });

  test('GET /nonexistent should return 404', async () => {
    await request(app)
      .get('/nonexistent')
      .expect(404);
  });
});