const express = require('express');
const authMiddleware = require('../middleware/authMiddleware');
const router = express.Router();

// Apply auth middleware to all routes in this router
router.use(authMiddleware);

router.get('/profile', (req, res) => {
  res.json({
    message: 'Protected profile data',
    user: req.user
  });
});

router.get('/dashboard', (req, res) => {
  res.json({
    message: 'Welcome to your dashboard',
    userId: req.user.userId,
    timestamp: new Date().toISOString()
  });
});

router.post('/data', (req, res) => {
  res.json({
    message: 'Data created successfully',
    userId: req.user.userId,
    data: req.body
  });
});

module.exports = router;