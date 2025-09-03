const AuthService = require('../src/services/authService');

describe('AuthService', () => {
  describe('generateToken', () => {
    it('should generate a valid token', () => {
      const token = AuthService.generateToken('user123');
      expect(typeof token).toBe('string');
      expect(token.length).toBeGreaterThan(0);
    });

    it('should throw error for missing userId', () => {
      expect(() => AuthService.generateToken()).toThrow('User ID is required');
    });
  });

  describe('verifyToken', () => {
    it('should verify a valid token', () => {
      const userId = 'user123';
      const token = AuthService.generateToken(userId);
      const decoded = AuthService.verifyToken(token);
      expect(decoded.userId).toBe(userId);
    });

    it('should throw error for invalid token', () => {
      expect(() => AuthService.verifyToken('invalid-token')).toThrow('Invalid or expired token');
    });

    it('should throw error for missing token', () => {
      expect(() => AuthService.verifyToken()).toThrow('Token is required');
    });
  });

  describe('password hashing', () => {
    it('should hash and compare passwords correctly', async () => {
      const password = 'testpassword';
      const hash = await AuthService.hashPassword(password);
      
      expect(hash).not.toBe(password);
      
      const isValid = await AuthService.comparePassword(password, hash);
      expect(isValid).toBe(true);
      
      const isInvalid = await AuthService.comparePassword('wrongpassword', hash);
      expect(isInvalid).toBe(false);
    });
  });
});