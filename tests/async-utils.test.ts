import { AsyncUtils } from '../src/async-utils';

describe('AsyncUtils', () => {
  describe('delay', () => {
    it('should resolve after specified time', async () => {
      const start = Date.now();
      await AsyncUtils.delay(50);
      const elapsed = Date.now() - start;
      
      expect(elapsed).toBeGreaterThanOrEqual(45); // Allow some tolerance
    });

    it('should throw error for negative delay', async () => {
      await expect(AsyncUtils.delay(-1)).rejects.toThrow('Delay must be non-negative');
    });

    it('should handle zero delay', async () => {
      await expect(AsyncUtils.delay(0)).resolves.toBeUndefined();
    });
  });

  describe('fetchData', () => {
    beforeEach(() => {
      jest.spyOn(AsyncUtils, 'delay').mockResolvedValue();
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    it('should return data for valid URL', async () => {
      const result = await AsyncUtils.fetchData('https://api.example.com');
      
      expect(result).toEqual({
        data: 'Response from https://api.example.com',
        timestamp: expect.any(Number)
      });
    });

    it('should throw error for URLs containing "error"', async () => {
      await expect(AsyncUtils.fetchData('https://api.example.com/error')).rejects.toThrow('Network error');
    });

    it('should throw error for empty URL', async () => {
      await expect(AsyncUtils.fetchData('')).rejects.toThrow('URL is required');
    });

    it('should call delay method', async () => {
      await AsyncUtils.fetchData('https://api.example.com');
      
      expect(AsyncUtils.delay).toHaveBeenCalledWith(100);
    });
  });
});