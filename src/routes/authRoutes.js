const express = require('express');
const AuthService = require('../services/authService');
const router = express.Router();

// Mock user database
const users = new Map();

router.post('/register', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    if (!username || !password) {
      return res.status(400).json({ 
        error: 'Username and password are required' 
      });
    }

    if (users.has(username)) {
      return res.status(409).json({ 
        error: 'User already exists' 
      });
    }

    const hashedPassword = await AuthService.hashPassword(password);
    const userId = Date.now().toString();
    
    users.set(username, { 
      id: userId, 
      username, 
      password: hashedPassword 
    });

    const token = AuthService.generateToken(userId);
    
    res.status(201).json({ 
      message: 'User registered successfully',
      token,
      user: { id: userId, username }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    if (!username || !password) {
      return res.status(400).json({ 
        error: 'Username and password are required' 
      });
    }

    const user = users.get(username);
    if (!user) {
      return res.status(401).json({ 
        error: 'Invalid credentials' 
      });
    }

    const isValidPassword = await AuthService.comparePassword(password, user.password);
    if (!isValidPassword) {
      return res.status(401).json({ 
        error: 'Invalid credentials' 
      });
    }

    const token = AuthService.generateToken(user.id);
    
    res.json({ 
      message: 'Login successful',
      token,
      user: { id: user.id, username: user.username }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;