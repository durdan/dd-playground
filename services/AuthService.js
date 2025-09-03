const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('../models/User');

class AuthService {
  constructor(userStore, jwtSecret = 'your-secret-key') {
    this.userStore = userStore;
    this.jwtSecret = jwtSecret;
  }

  async hashPassword(password) {
    return bcrypt.hash(password, 10);
  }

  async comparePassword(password, hashedPassword) {
    return bcrypt.compare(password, hashedPassword);
  }

  generateToken(userId) {
    return jwt.sign({ userId }, this.jwtSecret, { expiresIn: '24h' });
  }

  verifyToken(token) {
    try {
      return jwt.verify(token, this.jwtSecret);
    } catch (error) {
      throw new Error('Invalid token');
    }
  }

  async register(email, password) {
    const errors = User.validate(email, password);
    if (errors.length > 0) {
      throw new Error(errors.join(', '));
    }

    if (this.userStore.findByEmail(email)) {
      throw new Error('User already exists');
    }

    const hashedPassword = await this.hashPassword(password);
    const user = new User(email, hashedPassword);
    
    this.userStore.save(user);
    return user;
  }

  async login(email, password) {
    if (!email || !password) {
      throw new Error('Email and password are required');
    }

    const user = this.userStore.findByEmail(email);
    if (!user) {
      throw new Error('Invalid credentials');
    }

    const isValidPassword = await this.comparePassword(password, user.password);
    if (!isValidPassword) {
      throw new Error('Invalid credentials');
    }

    return user;
  }
}

module.exports = AuthService;