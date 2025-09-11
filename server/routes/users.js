const express = require('express');
const UserService = require('../services/userService');
const { authenticateToken } = require('../middleware/auth');

const router = express.Router();
const userService = new UserService();

router.get('/', authenticateToken, async (req, res) => {
  try {
    const users = await userService.getAllUsers();
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/:id', authenticateToken, async (req, res) => {
  try {
    const user = await userService.getUserById(req.params.id);
    res.json(user);
  } catch (error) {
    res.status(404).json({ error: error.message });
  }
});

router.post('/', authenticateToken, async (req, res) => {
  try {
    const user = await userService.createUser(req.body);
    res.status(201).json(user);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

router.put('/:id', authenticateToken, async (req, res) => {
  try {
    const user = await userService.updateUser(req.params.id, req.body);
    res.json(user);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

router.delete('/:id', authenticateToken, async (req, res) => {
  try {
    const user = await userService.deleteUser(req.params.id);
    res.json({ message: 'User deleted successfully', user });
  } catch (error) {
    res.status(404).json({ error: error.message });
  }
});

module.exports = router;