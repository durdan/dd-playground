export interface ValidationResult {
  isValid: boolean;
  errors: string[];
  userMessage?: string;
}

export class ValidationService {
  static validateChatMessage(message: string): ValidationResult {
    const errors: string[] = [];

    if (!message || message.trim().length === 0) {
      errors.push('Message cannot be empty');
    }

    if (message.length > 4000) {
      errors.push('Message too long (max 4000 characters)');
    }

    if (message.trim().length < 2) {
      errors.push('Message too short (min 2 characters)');
    }

    // Check for potentially harmful content
    const suspiciousPatterns = [
      /<script/i,
      /javascript:/i,
      /on\w+\s*=/i
    ];

    if (suspiciousPatterns.some(pattern => pattern.test(message))) {
      errors.push('Message contains potentially harmful content');
    }

    return {
      isValid: errors.length === 0,
      errors,
      userMessage: errors.length > 0 ? errors[0] : undefined
    };
  }

  static validateApiKey(apiKey: string): ValidationResult {
    const errors: string[] = [];

    if (!apiKey || apiKey.trim().length === 0) {
      errors.push('API key is required');
    }

    if (apiKey && apiKey.length < 10) {
      errors.push('API key appears to be invalid');
    }

    return {
      isValid: errors.length === 0,
      errors,
      userMessage: errors.length > 0 ? 'Please provide a valid API key' : undefined
    };
  }
}