import { StringUtils } from '../string';

describe('StringUtils', () => {
  describe('capitalize', () => {
    it('should capitalize first letter', () => {
      expect(StringUtils.capitalize('hello')).toBe('Hello');
    });

    it('should handle empty string', () => {
      expect(StringUtils.capitalize('')).toBe('');
    });

    it('should handle single character', () => {
      expect(StringUtils.capitalize('a')).toBe('A');
    });

    it('should throw error for non-string input', () => {
      expect(() => StringUtils.capitalize(123 as any)).toThrow('Input must be a string');
    });
  });

  describe('reverseWords', () => {
    it('should reverse word order', () => {
      expect(StringUtils.reverseWords('hello world')).toBe('world hello');
    });

    it('should handle single word', () => {
      expect(StringUtils.reverseWords('hello')).toBe('hello');
    });

    it('should handle empty string', () => {
      expect(StringUtils.reverseWords('')).toBe('');
    });

    it('should throw error for non-string input', () => {
      expect(() => StringUtils.reverseWords(null as any)).toThrow('Input must be a string');
    });
  });

  describe('isPalindrome', () => {
    it('should identify palindromes', () => {
      expect(StringUtils.isPalindrome('racecar')).toBe(true);
      expect(StringUtils.isPalindrome('A man a plan a canal Panama')).toBe(true);
    });

    it('should identify non-palindromes', () => {
      expect(StringUtils.isPalindrome('hello')).toBe(false);
    });

    it('should handle empty string', () => {
      expect(StringUtils.isPalindrome('')).toBe(true);
    });

    it('should throw error for non-string input', () => {
      expect(() => StringUtils.isPalindrome(123 as any)).toThrow('Input must be a string');
    });
  });
});