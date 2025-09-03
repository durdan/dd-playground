import { MathUtils } from '../math';

describe('MathUtils', () => {
  describe('add', () => {
    it('should add two positive numbers', () => {
      expect(MathUtils.add(2, 3)).toBe(5);
    });

    it('should add negative numbers', () => {
      expect(MathUtils.add(-2, -3)).toBe(-5);
    });

    it('should add zero', () => {
      expect(MathUtils.add(5, 0)).toBe(5);
    });

    it('should throw error for non-finite numbers', () => {
      expect(() => MathUtils.add(Infinity, 5)).toThrow('Both arguments must be finite numbers');
      expect(() => MathUtils.add(5, NaN)).toThrow('Both arguments must be finite numbers');
    });
  });

  describe('divide', () => {
    it('should divide two numbers', () => {
      expect(MathUtils.divide(10, 2)).toBe(5);
    });

    it('should handle negative division', () => {
      expect(MathUtils.divide(-10, 2)).toBe(-5);
    });

    it('should throw error for division by zero', () => {
      expect(() => MathUtils.divide(10, 0)).toThrow('Division by zero is not allowed');
    });

    it('should throw error for non-finite numbers', () => {
      expect(() => MathUtils.divide(Infinity, 5)).toThrow('Both arguments must be finite numbers');
    });
  });

  describe('factorial', () => {
    it('should calculate factorial of positive numbers', () => {
      expect(MathUtils.factorial(0)).toBe(1);
      expect(MathUtils.factorial(1)).toBe(1);
      expect(MathUtils.factorial(5)).toBe(120);
    });

    it('should throw error for negative numbers', () => {
      expect(() => MathUtils.factorial(-1)).toThrow('Factorial requires a non-negative integer');
    });

    it('should throw error for non-integers', () => {
      expect(() => MathUtils.factorial(3.5)).toThrow('Factorial requires a non-negative integer');
    });
  });
});