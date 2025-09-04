import { Calculator } from '../src/calculator';
import { formatCurrency } from '../src/utils';

describe('Integration Tests', () => {
  it('should calculate and format total price', () => {
    const calculator = new Calculator();
    const price = 29.99;
    const quantity = 3;
    const tax = 0.08;

    const subtotal = calculator.multiply(price, quantity);
    const taxAmount = calculator.multiply(subtotal, tax);
    const total = calculator.add(subtotal, taxAmount);

    expect(formatCurrency(total)).toBe('$97.17');
  });

  it('should handle discount calculation', () => {
    const calculator = new Calculator();
    const originalPrice = 100;
    const discountPercent = 0.15;

    const discountAmount = calculator.multiply(originalPrice, discountPercent);
    const finalPrice = calculator.subtract(originalPrice, discountAmount);

    expect(finalPrice).toBe(85);
    expect(formatCurrency(finalPrice)).toBe('$85.00');
  });
});