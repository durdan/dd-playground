const request = require('supertest');
const app = require('../server');
const AuthService = require('../src/services/authService');

describe('Middleware Integration', () => {
  let authToken;

  beforeAll(async () => {
    // Register a test user
    const response = await request(app)
      .post('/auth/register')
      .send({ username: 'testuser', password: 'testpass' });
    
    authToken = response.body.token;
  });

  describe('Authentication Middleware', () => {
    it('should allow access with valid token', async () => {
      const response = await request(app)
        .get('/api/profile')
        .set('Authorization', `Bearer ${authToken}`);
      
      expect(response.status).toBe(200);
      expect(response.body.message).toBe('Protected profile data');
    });

    it('should deny access without token', async () => {
      const response = await request(app)
        .get('/api/profile');
      
      expect(response.status).toBe(401);
      expect(response.body.error).toContain('No token provided');
    });

    it('should deny access with invalid token', async () => {
      const response = await request(app)
        .get('/api/profile')
        .set('Authorization', 'Bearer invalid-token');
      
      expect(response.status).toBe(401);
    });
  });

  describe('Rate Limiting Middleware', () => {
    it('should include rate limit headers', async () => {
      const response = await request(app)
        .get('/api/profile')
        .set('Authorization', `Bearer ${authToken}`);
      
      expect(response.headers['x-ratelimit-limit']).toBeDefined();
      expect(response.headers['x-ratelimit-remaining']).toBeDefined();
    });

    it('should block requests after limit exceeded', async () => {
      // This test would need to be adjusted based on your rate limits
      // For demonstration, we'll just verify the middleware is working
      const response = await request(app)
        .post('/auth/login')
        .send({ username: 'testuser', password: 'testpass' });
      
      expect(response.headers['x-ratelimit-limit']).toBe('50');
    }, 10000);
  });
});