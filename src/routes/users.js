const express = require('express');
const User = require('../models/User');
const { authenticateToken, generateToken } = require('../middleware/auth');
const { validateRequest } = require('../middleware/validation');
const Joi = require('joi');

const router = express.Router();

// In-memory storage for demo (replace with database)
let users = [];
let nextId = 1;

// GET /users
router.get('/', authenticateToken, (req, res) => {
  const publicUsers = users.map(user => user.toJSON());
  res.json(publicUsers);
});

// GET /users/:id
router.get('/:id', authenticateToken, (req, res) => {
  const id = parseInt(req.params.id);
  const user = users.find(u => u.id === id);
  
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  res.json(user.toJSON());
});

// POST /users
router.post('/', validateRequest(Joi.object({
  email: Joi.string().email().required(),
  name: Joi.string().min(2).max(50).required(),
  password: Joi.string().min(6).required()
})), async (req, res) => {
  try {
    // Check if user already exists
    const existingUser = users.find(u => u.email === req.body.email);
    if (existingUser) {
      return res.status(409).json({ error: 'User already exists' });
    }

    const userData = { ...req.body, id: nextId++ };
    const user = new User(userData);
    await user.hashPassword();
    
    users.push(user);
    
    const token = generateToken(user.id);
    res.status(201).json({ user: user.toJSON(), token });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// PUT /users/:id
router.put('/:id', authenticateToken, validateRequest(Joi.object({
  email: Joi.string().email(),
  name: Joi.string().min(2).max(50),
  password: Joi.string().min(6)
}).min(1)), async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const userIndex = users.findIndex(u => u.id === id);
    
    if (userIndex === -1) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    const user = users[userIndex];
    Object.assign(user, req.body);
    
    if (req.body.password) {
      await user.hashPassword();
    }
    
    res.json(user.toJSON());
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// DELETE /users/:id
router.delete('/:id', authenticateToken, (req, res) => {
  const id = parseInt(req.params.id);
  const userIndex = users.findIndex(u => u.id === id);
  
  if (userIndex === -1) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  users.splice(userIndex, 1);
  res.status(204).send();
});

module.exports = router;