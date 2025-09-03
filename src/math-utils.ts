export const delay = (ms: number): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

export const factorial = (n: number): number => {
  if (!Number.isInteger(n) || n < 0) {
    throw new Error('Factorial is only defined for non-negative integers');
  }
  
  if (n === 0 || n === 1) {
    return 1;
  }
  
  return n * factorial(n - 1);
};

export const isPrime = (n: number): boolean => {
  if (!Number.isInteger(n) || n < 2) {
    return false;
  }
  
  for (let i = 2; i <= Math.sqrt(n); i++) {
    if (n % i === 0) {
      return false;
    }
  }
  
  return true;
};