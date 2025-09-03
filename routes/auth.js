const express = require('express');
const AuthController = require('../controllers/AuthController');
const authMiddleware = require('../middleware/auth');

function createAuthRoutes(authService) {
  const router = express.Router();
  const authController = new AuthController(authService);

  router.post('/register', (req, res) => authController.register(req, res));
  router.post('/login', (req, res) => authController.login(req, res));
  router.post('/logout', authMiddleware(authService), (req, res) => authController.logout(req, res));

  return router;
}

module.exports = createAuthRoutes;