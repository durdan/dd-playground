const request = require('supertest');
const app = require('../src/app');

describe('API Endpoints', () => {
  test('GET /health should return healthy status', async () => {
    const response = await request(app)
      .get('/health')
      .expect(200);
    
    expect(response.body.status).toBe('healthy');
    expect(response.body.timestamp).toBeDefined();
  });

  test('GET /api/users should return users array', async () => {
    const response = await request(app)
      .get('/api/users')
      .expect(200);
    
    expect(Array.isArray(response.body)).toBe(true);
  });

  test('POST /api/users should create user with valid data', async () => {
    const userData = {
      name: 'Test User',
      email: 'test@example.com'
    };

    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(201);
    
    expect(response.body.name).toBe(userData.name);
    expect(response.body.email).toBe(userData.email);
    expect(response.body.id).toBeDefined();
  });

  test('POST /api/users should reject invalid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Test User' }) // missing email
      .expect(400);
    
    expect(response.body.error).toBe('Name and email are required');
  });
});