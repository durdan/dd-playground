import { AsyncUtils } from '../src/async-utils';

describe('AsyncUtils', () => {
  describe('delay', () => {
    it('should delay for specified milliseconds', async () => {
      const start = Date.now();
      await AsyncUtils.delay(100);
      const end = Date.now();
      
      expect(end - start).toBeGreaterThanOrEqual(90); // Allow some tolerance
    });

    it('should throw error for negative delay', async () => {
      await expect(AsyncUtils.delay(-1)).rejects.toThrow('Delay must be non-negative');
    });

    it('should handle zero delay', async () => {
      const start = Date.now();
      await AsyncUtils.delay(0);
      const end = Date.now();
      
      expect(end - start).toBeLessThan(50);
    });
  });

  describe('fetchData', () => {
    beforeEach(() => {
      jest.spyOn(AsyncUtils, 'delay').mockResolvedValue();
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    it('should fetch data successfully', async () => {
      const url = 'https://api.example.com/data';
      const result = await AsyncUtils.fetchData(url);

      expect(result).toEqual({
        data: `Response from ${url}`,
        timestamp: expect.any(Number)
      });
      expect(AsyncUtils.delay).toHaveBeenCalledWith(100);
    });

    it('should throw error for empty URL', async () => {
      await expect(AsyncUtils.fetchData('')).rejects.toThrow('URL is required');
    });

    it('should throw network error for error URLs', async () => {
      await expect(AsyncUtils.fetchData('https://api.example.com/error')).rejects.toThrow('Network error');
    });
  });
});