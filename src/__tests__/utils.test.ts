import { delay, formatCurrency, capitalize } from '../utils';

describe('Utils', () => {
  describe('delay', () => {
    it('should resolve after specified time', async () => {
      const start = Date.now();
      await delay(100);
      const end = Date.now();
      
      expect(end - start).toBeGreaterThanOrEqual(90); // Allow some tolerance
    });
  });

  describe('formatCurrency', () => {
    it('should format currency with default USD', () => {
      expect(formatCurrency(1234.56)).toBe('$1,234.56');
    });

    it('should format currency with specified currency', () => {
      expect(formatCurrency(1234.56, 'EUR')).toBe('€1,234.56');
    });

    it('should handle zero amount', () => {
      expect(formatCurrency(0)).toBe('$0.00');
    });

    it('should throw error for invalid amount', () => {
      expect(() => formatCurrency(NaN)).toThrow('Amount must be a valid number');
      expect(() => formatCurrency('123' as any)).toThrow('Amount must be a valid number');
    });
  });

  describe('capitalize', () => {
    it('should capitalize first letter', () => {
      expect(capitalize('hello')).toBe('Hello');
    });

    it('should handle single character', () => {
      expect(capitalize('a')).toBe('A');
    });

    it('should handle empty string', () => {
      expect(capitalize('')).toBe('');
    });

    it('should convert rest to lowercase', () => {
      expect(capitalize('hELLO')).toBe('Hello');
    });

    it('should throw error for non-string input', () => {
      expect(() => capitalize(123 as any)).toThrow('Input must be a string');
    });
  });
});