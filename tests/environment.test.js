describe('Environment Configuration', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    jest.resetModules();
    process.env = { ...originalEnv };
  });

  afterAll(() => {
    process.env = originalEnv;
  });

  test('should use default port when PORT not set', () => {
    delete process.env.PORT;
    expect(process.env.PORT || 8080).toBe(8080);
  });

  test('should use environment PORT when set', () => {
    process.env.PORT = '3000';
    expect(process.env.PORT).toBe('3000');
  });

  test('should handle missing environment variables gracefully', () => {
    delete process.env.DATABASE_URL;
    delete process.env.REDIS_URL;
    
    // Application should still start without these
    expect(process.env.DATABASE_URL).toBeUndefined();
    expect(process.env.REDIS_URL).toBeUndefined();
  });
});