export class MathUtils {
  static add(a: number, b: number): number {
    if (!Number.isFinite(a) || !Number.isFinite(b)) {
      throw new Error('Both arguments must be finite numbers');
    }
    return a + b;
  }

  static divide(a: number, b: number): number {
    if (!Number.isFinite(a) || !Number.isFinite(b)) {
      throw new Error('Both arguments must be finite numbers');
    }
    if (b === 0) {
      throw new Error('Division by zero is not allowed');
    }
    return a / b;
  }

  static factorial(n: number): number {
    if (!Number.isInteger(n) || n < 0) {
      throw new Error('Factorial requires a non-negative integer');
    }
    if (n === 0 || n === 1) return 1;
    return n * this.factorial(n - 1);
  }
}