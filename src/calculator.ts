export class Calculator {
  add(a: number, b: number): number {
    if (!this.isValidNumber(a) || !this.isValidNumber(b)) {
      throw new Error('Invalid input: arguments must be numbers');
    }
    return a + b;
  }

  subtract(a: number, b: number): number {
    if (!this.isValidNumber(a) || !this.isValidNumber(b)) {
      throw new Error('Invalid input: arguments must be numbers');
    }
    return a - b;
  }

  multiply(a: number, b: number): number {
    if (!this.isValidNumber(a) || !this.isValidNumber(b)) {
      throw new Error('Invalid input: arguments must be numbers');
    }
    return a * b;
  }

  divide(a: number, b: number): number {
    if (!this.isValidNumber(a) || !this.isValidNumber(b)) {
      throw new Error('Invalid input: arguments must be numbers');
    }
    if (b === 0) {
      throw new Error('Division by zero is not allowed');
    }
    return a / b;
  }

  private isValidNumber(value: any): value is number {
    return typeof value === 'number' && !isNaN(value) && isFinite(value);
  }
}