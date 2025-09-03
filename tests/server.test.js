const request = require('supertest');
const app = require('../src/server');

describe('Server Endpoints', () => {
  test('GET /health returns healthy status', async () => {
    const response = await request(app)
      .get('/health')
      .expect(200);
    
    expect(response.body.status).toBe('healthy');
    expect(response.body.environment).toBeDefined();
  });

  test('GET /api/status returns API status', async () => {
    const response = await request(app)
      .get('/api/status')
      .expect(200);
    
    expect(response.body.message).toBe('API is running');
    expect(response.body.environment).toBeDefined();
  });

  test('GET /metrics returns prometheus metrics', async () => {
    const response = await request(app)
      .get('/metrics')
      .expect(200);
    
    expect(response.text).toContain('http_requests_total');
    expect(response.headers['content-type']).toContain('text/plain');
  });

  test('Invalid endpoint returns 404', async () => {
    await request(app)
      .get('/invalid-endpoint')
      .expect(404);
  });
});