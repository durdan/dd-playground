describe('App Tests', () => {
  test('should have models', () => {
    const { User, Product } = require('../src/models');
    const user = new User('Test', 'test@example.com');
    expect(user.validate()).toBe(true);
  });

  test('should have config', () => {
    const config = require('../config/config');
    expect(config.port).toBeDefined();
  });
});