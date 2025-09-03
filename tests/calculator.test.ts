import { Calculator } from '../src/calculator';

describe('Calculator', () => {
  let calculator: Calculator;

  beforeEach(() => {
    calculator = new Calculator();
  });

  describe('add', () => {
    it('should add two positive numbers correctly', () => {
      expect(calculator.add(2, 3)).toBe(5);
    });

    it('should add negative numbers correctly', () => {
      expect(calculator.add(-2, -3)).toBe(-5);
    });

    it('should add zero correctly', () => {
      expect(calculator.add(5, 0)).toBe(5);
    });

    it('should throw error for non-number inputs', () => {
      expect(() => calculator.add('2' as any, 3)).toThrow('Both arguments must be numbers');
      expect(() => calculator.add(2, null as any)).toThrow('Both arguments must be numbers');
    });
  });

  describe('subtract', () => {
    it('should subtract numbers correctly', () => {
      expect(calculator.subtract(5, 3)).toBe(2);
      expect(calculator.subtract(3, 5)).toBe(-2);
    });
  });

  describe('multiply', () => {
    it('should multiply numbers correctly', () => {
      expect(calculator.multiply(4, 3)).toBe(12);
      expect(calculator.multiply(-2, 3)).toBe(-6);
    });
  });

  describe('divide', () => {
    it('should divide numbers correctly', () => {
      expect(calculator.divide(10, 2)).toBe(5);
      expect(calculator.divide(7, 2)).toBe(3.5);
    });

    it('should throw error when dividing by zero', () => {
      expect(() => calculator.divide(5, 0)).toThrow('Division by zero is not allowed');
    });
  });
});