const express = require('express');
const eventController = require('../controllers/eventController');

const router = express.Router();

// GET /api/events/latest - Get latest events
router.get('/latest', eventController.getLatestEvents);

// GET /api/events/upcoming - Get upcoming events
router.get('/upcoming', eventController.getUpcomingEvents);

// GET /api/events/:id - Get event details by ID
router.get('/:id', eventController.getEventDetails);

module.exports = router;