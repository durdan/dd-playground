const request = require('supertest');
const app = require('../app');

describe('Application Endpoints', () => {
  test('GET /health returns healthy status', async () => {
    const response = await request(app)
      .get('/health')
      .expect(200);
    
    expect(response.body.status).toBe('healthy');
    expect(response.body.environment).toBeDefined();
  });

  test('GET /metrics returns prometheus metrics', async () => {
    const response = await request(app)
      .get('/metrics')
      .expect(200);
    
    expect(response.text).toContain('http_requests_total');
  });

  test('GET /api/status returns API status', async () => {
    const response = await request(app)
      .get('/api/status')
      .expect(200);
    
    expect(response.body.message).toBe('API is running');
  });

  test('GET /env-info returns 404 in non-staging environment', async () => {
    const originalEnv = process.env.NODE_ENV;
    process.env.NODE_ENV = 'production';
    
    await request(app)
      .get('/env-info')
      .expect(404);
    
    process.env.NODE_ENV = originalEnv;
  });
});