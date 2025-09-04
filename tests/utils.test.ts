import { delay, formatCurrency, capitalize } from '../src/utils';

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
    it('should format currency correctly', () => {
      expect(formatCurrency(1234.56)).toBe('$1,234.56');
      expect(formatCurrency(0)).toBe('$0.00');
      expect(formatCurrency(1234.56, 'EUR')).toBe('€1,234.56');
    });

    it('should throw error for invalid input', () => {
      expect(() => formatCurrency(NaN)).toThrow('Amount must be a valid number');
      expect(() => formatCurrency('123' as any)).toThrow('Amount must be a valid number');
    });
  });

  describe('capitalize', () => {
    it('should capitalize strings correctly', () => {
      expect(capitalize('hello')).toBe('Hello');
      expect(capitalize('WORLD')).toBe('World');
      expect(capitalize('hELLo WoRLD')).toBe('Hello world');
      expect(capitalize('')).toBe('');
    });

    it('should throw error for non-string input', () => {
      expect(() => capitalize(123 as any)).toThrow('Input must be a string');
      expect(() => capitalize(null as any)).toThrow('Input must be a string');
    });
  });
});