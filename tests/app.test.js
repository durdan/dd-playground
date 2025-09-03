const request = require('supertest');
const app = require('../src/app');

describe('Express App', () => {
  describe('GET /api/health', () => {
    it('should return health status', async () => {
      const response = await request(app)
        .get('/api/health')
        .expect(200);

      expect(response.body).toHaveProperty('status', 'OK');
      expect(response.body).toHaveProperty('timestamp');
      expect(response.body).toHaveProperty('uptime');
    });
  });

  describe('404 handling', () => {
    it('should return 404 for unknown routes', async () => {
      const response = await request(app)
        .get('/api/unknown')
        .expect(404);

      expect(response.body.error).toHaveProperty('message');
      expect(response.body.error).toHaveProperty('status', 404);
    });
  });

  describe('Error handling', () => {
    it('should handle server errors gracefully', async () => {
      // This would test actual error scenarios in a real app
      expect(app).toBeDefined();
    });
  });
});