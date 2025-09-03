const request = require('supertest');
const app = require('../src/server');

describe('Server Endpoints', () => {
  test('GET /health returns healthy status', async () => {
    const response = await request(app)
      .get('/health')
      .expect(200);

    expect(response.body.status).toBe('healthy');
    expect(response.body.environment).toBeDefined();
    expect(response.body.uptime).toBeGreaterThanOrEqual(0);
  });

  test('GET /metrics returns prometheus metrics', async () => {
    const response = await request(app)
      .get('/metrics')
      .expect(200);

    expect(response.text).toContain('http_requests_total');
    expect(response.text).toContain('http_request_duration_seconds');
  });

  test('GET /api/status returns API status', async () => {
    const response = await request(app)
      .get('/api/status')
      .expect(200);

    expect(response.body.message).toBe('API is running');
    expect(response.body.timestamp).toBeDefined();
  });

  test('GET /env-info returns environment info in staging', async () => {
    process.env.NODE_ENV = 'staging';
    process.env.API_KEY = 'test-key';
    
    const response = await request(app)
      .get('/env-info')
      .expect(200);

    expect(response.body.environment).toBe('staging');
    expect(response.body.hasApiKey).toBe(true);
  });

  test('GET /env-info returns 404 in non-staging environment', async () => {
    process.env.NODE_ENV = 'production';
    
    await request(app)
      .get('/env-info')
      .expect(404);
  });
});