const Event = require('../models/Event');

class EventService {
  constructor() {
    // Mock data - in real app, this would be a database
    this.events = [
      new Event({
        id: 1,
        title: 'Tech Conference 2024',
        description: 'Annual technology conference',
        startDate: '2024-06-15T09:00:00Z',
        endDate: '2024-06-15T17:00:00Z',
        location: 'San Francisco, CA',
        createdAt: '2024-01-15T10:00:00Z'
      }),
      new Event({
        id: 2,
        title: 'Workshop: React Basics',
        description: 'Learn React fundamentals',
        startDate: '2024-12-20T14:00:00Z',
        endDate: '2024-12-20T16:00:00Z',
        location: 'Online',
        createdAt: '2024-01-20T11:00:00Z'
      }),
      new Event({
        id: 3,
        title: 'Team Building Event',
        description: 'Company team building activities',
        startDate: '2024-12-25T10:00:00Z',
        endDate: '2024-12-25T15:00:00Z',
        location: 'Central Park, NY',
        createdAt: '2024-01-10T09:00:00Z'
      })
    ];
  }

  getLatestEvents(limit = 10) {
    return this.events
      .sort((a, b) => b.createdAt - a.createdAt)
      .slice(0, limit);
  }

  getUpcomingEvents(limit = 10) {
    const now = new Date();
    return this.events
      .filter(event => event.startDate > now)
      .sort((a, b) => a.startDate - b.startDate)
      .slice(0, limit);
  }

  getEventById(id) {
    const event = this.events.find(event => event.id === parseInt(id));
    if (!event) {
      throw new Error('Event not found');
    }
    return event;
  }
}

module.exports = new EventService();