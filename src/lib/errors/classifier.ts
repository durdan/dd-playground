// src/lib/errors/classifier.ts

/**
 * ErrorClassifier class to categorize syntax errors, provide contextual messages,
 * and suggest fixes based on common patterns.
 */
export class ErrorClassifier {
  /**
   * Classify the given syntax error and suggest fixes.
   * @param error The syntax error to classify.
   * @returns An object containing the error category, message, and suggested fixes.
   */
  classifyError(error: SyntaxError): { category: string; message: string; suggestions: string[] } {
    // Example error patterns and fixes
    const patterns = [
      {
        pattern: /Unexpected token (.+)/,
        category: 'Syntax Error',
        message: 'Unexpected token encountered in the code',
        suggestions: ['Check for missing operators', 'Verify if all brackets are correctly closed'],
      },
      {
        pattern: /'([^']+)' is not defined/,
        category: 'Reference Error',
        message: 'Variable or function is not defined',
        suggestions: ['Declare the variable before use', 'Check for any typo in the variable name'],
      },
    ];

    for (const { pattern, category, message, suggestions } of patterns) {
      const match = error.message.match(pattern);
      if (match) {
        return { category, message, suggestions };
      }
    }

    // Default case if the error does not match any known patterns
    return {
      category: 'Unknown Error',
      message: 'An unknown error occurred',
      suggestions: ['Review the error message for details', 'Consult documentation or seek help from forums'],
    };
  }
}
