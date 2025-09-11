const eventService = require('../services/eventService');
const { formatResponse, formatError } = require('../utils/responseFormatter');

class EventController {
  async getLatestEvents(req, res, next) {
    try {
      const limit = parseInt(req.query.limit) || 10;
      
      if (limit < 1 || limit > 100) {
        return res.status(400).json(
          formatError('Limit must be between 1 and 100', 400)
        );
      }

      const events = eventService.getLatestEvents(limit);
      res.json(formatResponse(events, 'Latest events retrieved successfully'));
    } catch (error) {
      next(error);
    }
  }

  async getUpcomingEvents(req, res, next) {
    try {
      const limit = parseInt(req.query.limit) || 10;
      
      if (limit < 1 || limit > 100) {
        return res.status(400).json(
          formatError('Limit must be between 1 and 100', 400)
        );
      }

      const events = eventService.getUpcomingEvents(limit);
      res.json(formatResponse(events, 'Upcoming events retrieved successfully'));
    } catch (error) {
      next(error);
    }
  }

  async getEventDetails(req, res, next) {
    try {
      const { id } = req.params;
      
      if (!id || isNaN(parseInt(id))) {
        return res.status(400).json(
          formatError('Valid event ID is required', 400)
        );
      }

      const event = eventService.getEventById(id);
      res.json(formatResponse(event, 'Event details retrieved successfully'));
    } catch (error) {
      if (error.message === 'Event not found') {
        return res.status(404).json(formatError(error.message, 404));
      }
      next(error);
    }
  }
}

module.exports = new EventController();