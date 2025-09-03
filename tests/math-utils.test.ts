import { delay, factorial, isPrime } from '../src/math-utils';

describe('Math Utils', () => {
  describe('delay', () => {
    it('should resolve after specified time', async () => {
      const start = Date.now();
      await delay(100);
      const end = Date.now();
      
      expect(end - start).toBeGreaterThanOrEqual(90); // Allow some tolerance
    });
  });

  describe('factorial', () => {
    it('should calculate factorial correctly', () => {
      expect(factorial(0)).toBe(1);
      expect(factorial(1)).toBe(1);
      expect(factorial(5)).toBe(120);
      expect(factorial(3)).toBe(6);
    });

    it('should throw error for negative numbers', () => {
      expect(() => factorial(-1)).toThrow('Factorial is only defined for non-negative integers');
    });

    it('should throw error for non-integers', () => {
      expect(() => factorial(3.5)).toThrow('Factorial is only defined for non-negative integers');
    });
  });

  describe('isPrime', () => {
    it('should identify prime numbers correctly', () => {
      expect(isPrime(2)).toBe(true);
      expect(isPrime(3)).toBe(true);
      expect(isPrime(17)).toBe(true);
      expect(isPrime(97)).toBe(true);
    });

    it('should identify non-prime numbers correctly', () => {
      expect(isPrime(1)).toBe(false);
      expect(isPrime(4)).toBe(false);
      expect(isPrime(15)).toBe(false);
      expect(isPrime(100)).toBe(false);
    });

    it('should return false for negative numbers and zero', () => {
      expect(isPrime(0)).toBe(false);
      expect(isPrime(-5)).toBe(false);
    });
  });
});