export function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export function formatCurrency(amount: number, currency: string = 'USD'): string {
  if (typeof amount !== 'number' || isNaN(amount)) {
    throw new Error('Amount must be a valid number');
  }
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency
  }).format(amount);
}

export function capitalize(str: string): string {
  if (typeof str !== 'string') {
    throw new Error('Input must be a string');
  }
  
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}