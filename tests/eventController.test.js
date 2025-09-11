const request = require('supertest');
const app = require('../app');

describe('Event API Endpoints', () => {
  describe('GET /api/events/latest', () => {
    it('should return latest events successfully', async () => {
      const response = await request(app)
        .get('/api/events/latest')
        .expect(200);

      expect(response.body.status).toBe('success');
      expect(response.body.data).toBeInstanceOf(Array);
      expect(response.body.message).toBe('Latest events retrieved successfully');
    });

    it('should respect limit parameter', async () => {
      const response = await request(app)
        .get('/api/events/latest?limit=2')
        .expect(200);

      expect(response.body.data.length).toBeLessThanOrEqual(2);
    });

    it('should reject invalid limit', async () => {
      const response = await request(app)
        .get('/api/events/latest?limit=101')
        .expect(400);

      expect(response.body.status).toBe('error');
      expect(response.body.message).toBe('Limit must be between 1 and 100');
    });
  });

  describe('GET /api/events/upcoming', () => {
    it('should return upcoming events successfully', async () => {
      const response = await request(app)
        .get('/api/events/upcoming')
        .expect(200);

      expect(response.body.status).toBe('success');
      expect(response.body.data).toBeInstanceOf(Array);
      expect(response.body.message).toBe('Upcoming events retrieved successfully');
    });

    it('should return events in chronological order', async () => {
      const response = await request(app)
        .get('/api/events/upcoming')
        .expect(200);

      const events = response.body.data;
      for (let i = 1; i < events.length; i++) {
        const prevDate = new Date(events[i - 1].startDate);
        const currDate = new Date(events[i].startDate);
        expect(prevDate.getTime()).toBeLessThanOrEqual(currDate.getTime());
      }
    });
  });

  describe('GET /api/events/:id', () => {
    it('should return event details for valid ID', async () => {
      const response = await request(app)
        .get('/api/events/1')
        .expect(200);

      expect(response.body.status).toBe('success');
      expect(response.body.data.id).toBe(1);
      expect(response.body.data.title).toBeDefined();
    });

    it('should return 404 for non-existent event', async () => {
      const response = await request(app)
        .get('/api/events/999')
        .expect(404);

      expect(response.body.status).toBe('error');
      expect(response.body.message).toBe('Event not found');
    });

    it('should return 400 for invalid ID', async () => {
      const response = await request(app)
        .get('/api/events/invalid')
        .expect(400);

      expect(response.body.status).toBe('error');
      expect(response.body.message).toBe('Valid event ID is required');
    });
  });

  describe('Error handling', () => {
    it('should return 404 for non-existent routes', async () => {
      const response = await request(app)
        .get('/api/nonexistent')
        .expect(404);

      expect(response.body.status).toBe('error');
      expect(response.body.message).toBe('Route not found');
    });
  });
});