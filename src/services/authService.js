const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';
const JWT_EXPIRES_IN = '1h';

class AuthService {
  static generateToken(userId) {
    if (!userId) {
      throw new Error('User ID is required');
    }
    return jwt.sign({ userId }, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN });
  }

  static verifyToken(token) {
    if (!token) {
      throw new Error('Token is required');
    }
    try {
      return jwt.verify(token, JWT_SECRET);
    } catch (error) {
      throw new Error('Invalid or expired token');
    }
  }

  static async hashPassword(password) {
    if (!password) {
      throw new Error('Password is required');
    }
    return bcrypt.hash(password, 10);
  }

  static async comparePassword(password, hash) {
    if (!password || !hash) {
      throw new Error('Password and hash are required');
    }
    return bcrypt.compare(password, hash);
  }
}

module.exports = AuthService;