const eventService = require('../services/eventService');

describe('EventService', () => {
  describe('getLatestEvents', () => {
    it('should return events sorted by creation date', () => {
      const events = eventService.getLatestEvents();
      
      expect(events).toBeInstanceOf(Array);
      expect(events.length).toBeGreaterThan(0);
      
      // Check if sorted by createdAt descending
      for (let i = 1; i < events.length; i++) {
        expect(events[i - 1].createdAt.getTime())
          .toBeGreaterThanOrEqual(events[i].createdAt.getTime());
      }
    });

    it('should respect limit parameter', () => {
      const events = eventService.getLatestEvents(2);
      expect(events.length).toBeLessThanOrEqual(2);
    });
  });

  describe('getUpcomingEvents', () => {
    it('should return only future events', () => {
      const events = eventService.getUpcomingEvents();
      const now = new Date();
      
      events.forEach(event => {
        expect(event.startDate.getTime()).toBeGreaterThan(now.getTime());
      });
    });

    it('should return events sorted by start date', () => {
      const events = eventService.getUpcomingEvents();
      
      for (let i = 1; i < events.length; i++) {
        expect(events[i - 1].startDate.getTime())
          .toBeLessThanOrEqual(events[i].startDate.getTime());
      }
    });
  });

  describe('getEventById', () => {
    it('should return event for valid ID', () => {
      const event = eventService.getEventById(1);
      expect(event.id).toBe(1);
      expect(event.title).toBeDefined();
    });

    it('should throw error for non-existent ID', () => {
      expect(() => {
        eventService.getEventById(999);
      }).toThrow('Event not found');
    });
  });
});