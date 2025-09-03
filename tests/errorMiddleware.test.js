const request = require('supertest');
const app = require('../src/app');

describe('Error Handling Middleware', () => {
  describe('Success Cases', () => {
    test('should return success response', async () => {
      const response = await request(app)
        .get('/api/success')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.message).toBe('Everything works!');
    });
  });

  describe('Validation Errors', () => {
    test('should handle validation errors with details', async () => {
      const response = await request(app)
        .post('/api/validate')
        .send({ email: 'invalid', age: 16 })
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('VALIDATION_ERROR');
      expect(response.body.error.details).toHaveLength(2);
      expect(response.body.error.details[0].field).toBe('email');
      expect(response.body.error.details[1].field).toBe('age');
    });

    test('should pass validation with valid data', async () => {
      const response = await request(app)
        .post('/api/validate')
        .send({ email: 'test@example.com', age: 25 })
        .expect(200);

      expect(response.body.success).toBe(true);
    });
  });

  describe('Not Found Errors', () => {
    test('should handle resource not found', async () => {
      const response = await request(app)
        .get('/api/user/999')
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('NOT_FOUND');
      expect(response.body.error.message).toBe('User not found');
    });

    test('should handle route not found', async () => {
      const response = await request(app)
        .get('/api/nonexistent')
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('ROUTE_NOT_FOUND');
    });
  });

  describe('Authorization Errors', () => {
    test('should handle unauthorized access', async () => {
      const response = await request(app)
        .get('/api/protected')
        .expect(401);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('UNAUTHORIZED');
    });

    test('should allow access with token', async () => {
      const response = await request(app)
        .get('/api/protected')
        .set('Authorization', 'Bearer token')
        .expect(200);

      expect(response.body.success).toBe(true);
    });
  });

  describe('Conflict Errors', () => {
    test('should handle resource conflicts', async () => {
      const response = await request(app)
        .post('/api/user')
        .send({ email: 'taken@example.com' })
        .expect(409);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('CONFLICT');
    });
  });

  describe('Async Errors', () => {
    test('should handle async errors', async () => {
      const response = await request(app)
        .get('/api/async-error')
        .expect(500);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('INTERNAL_ERROR');
    });
  });

  describe('Unhandled Errors', () => {
    test('should handle unhandled synchronous errors', async () => {
      const response = await request(app)
        .get('/api/unhandled')
        .expect(500);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('INTERNAL_ERROR');
    });
  });
});