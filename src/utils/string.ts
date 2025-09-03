export class StringUtils {
  static capitalize(str: string): string {
    if (typeof str !== 'string') {
      throw new Error('Input must be a string');
    }
    if (str.length === 0) return str;
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
  }

  static reverseWords(str: string): string {
    if (typeof str !== 'string') {
      throw new Error('Input must be a string');
    }
    return str.split(' ').reverse().join(' ');
  }

  static isPalindrome(str: string): boolean {
    if (typeof str !== 'string') {
      throw new Error('Input must be a string');
    }
    const cleaned = str.toLowerCase().replace(/[^a-z0-9]/g, '');
    return cleaned === cleaned.split('').reverse().join('');
  }
}