const User = require('../../src/models/User');

describe('User Model', () => {
  describe('constructor', () => {
    it('should create user with provided data', () => {
      const userData = {
        id: 1,
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123'
      };
      
      const user = new User(userData);
      
      expect(user.id).toBe(1);
      expect(user.email).toBe('test@example.com');
      expect(user.name).toBe('Test User');
      expect(user.password).toBe('password123');
      expect(user.createdAt).toBeInstanceOf(Date);
    });

    it('should set createdAt to current date if not provided', () => {
      const user = new User({ email: 'test@example.com', name: 'Test' });
      expect(user.createdAt).toBeInstanceOf(Date);
    });
  });

  describe('validate', () => {
    it('should validate correct user data', () => {
      const userData = {
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123'
      };
      
      const { error } = User.validate(userData);
      expect(error).toBeUndefined();
    });

    it('should reject invalid email', () => {
      const userData = {
        email: 'invalid-email',
        name: 'Test User',
        password: 'password123'
      };
      
      const { error } = User.validate(userData);
      expect(error).toBeDefined();
      expect(error.details[0].path).toContain('email');
    });

    it('should reject short password', () => {
      const userData = {
        email: 'test@example.com',
        name: 'Test User',
        password: '123'
      };
      
      const { error } = User.validate(userData);
      expect(error).toBeDefined();
      expect(error.details[0].path).toContain('password');
    });

    it('should reject missing required fields', () => {
      const { error } = User.validate({});
      expect(error).toBeDefined();
      expect(error.details).toHaveLength(3);
    });
  });

  describe('validateUpdate', () => {
    it('should validate partial update data', () => {
      const { error } = User.validateUpdate({ name: 'New Name' });
      expect(error).toBeUndefined();
    });

    it('should reject empty update', () => {
      const { error } = User.validateUpdate({});
      expect(error).toBeDefined();
    });
  });

  describe('hashPassword', () => {
    it('should hash the password', async () => {
      const user = new User({
        email: 'test@example.com',
        name: 'Test',
        password: 'plaintext'
      });
      
      await user.hashPassword();
      
      expect(user.password).not.toBe('plaintext');
      expect(user.password).toMatch(/^\$2b\$10\$/);
    });

    it('should not hash if password is undefined', async () => {
      const user = new User({ email: 'test@example.com', name: 'Test' });
      await user.hashPassword();
      expect(user.password).toBeUndefined();
    });
  });

  describe('comparePassword', () => {
    it('should return true for correct password', async () => {
      const user = new User({
        email: 'test@example.com',
        name: 'Test',
        password: 'plaintext'
      });
      
      await user.hashPassword();
      const isMatch = await user.comparePassword('plaintext');
      
      expect(isMatch).toBe(true);
    });

    it('should return false for incorrect password', async () => {
      const user = new User({
        email: 'test@example.com',
        name: 'Test',
        password: 'plaintext'
      });
      
      await user.hashPassword();
      const isMatch = await user.comparePassword('wrongpassword');
      
      expect(isMatch).toBe(false);
    });
  });

  describe('toJSON', () => {
    it('should exclude password from JSON representation', () => {
      const user = new User({
        id: 1,
        email: 'test@example.com',
        name: 'Test User',
        password: 'secret'
      });
      
      const json = user.toJSON();
      
      expect(json.password).toBeUndefined();
      expect(json.id).toBe(1);
      expect(json.email).toBe('test@example.com');
      expect(json.name).toBe('Test User');
    });
  });
});