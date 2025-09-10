import { AppError, ErrorType, RecoveryOption, ErrorContext } from './ErrorTypes';

export class ErrorHandler {
  private static instance: ErrorHandler;
  private errorListeners: ((error: AppError, context: ErrorContext) => void)[] = [];

  static getInstance(): ErrorHandler {
    if (!ErrorHandler.instance) {
      ErrorHandler.instance = new ErrorHandler();
    }
    return ErrorHandler.instance;
  }

  handleError(error: any, context: ErrorContext): AppError {
    const appError = this.normalizeError(error, context);
    
    // Log error for debugging
    console.error(`[${appError.type}] ${context.component}:${context.action}`, {
      error: appError,
      context
    });

    // Notify listeners
    this.errorListeners.forEach(listener => {
      try {
        listener(appError, context);
      } catch (e) {
        console.error('Error in error listener:', e);
      }
    });

    return appError;
  }

  private normalizeError(error: any, context: ErrorContext): AppError {
    const timestamp = new Date();

    // Network errors
    if (error.name === 'NetworkError' || error.code === 'NETWORK_ERROR') {
      return {
        type: ErrorType.NETWORK,
        message: error.message || 'Network request failed',
        userMessage: 'Connection problem. Please check your internet and try again.',
        code: error.code,
        recoverable: true,
        retryable: true,
        timestamp
      };
    }

    // Rate limit errors
    if (error.status === 429 || error.code === 'RATE_LIMIT') {
      return {
        type: ErrorType.RATE_LIMIT,
        message: 'Rate limit exceeded',
        userMessage: 'Too many requests. Please wait a moment before trying again.',
        code: 'RATE_LIMIT',
        recoverable: true,
        retryable: true,
        timestamp
      };
    }

    // Authentication errors
    if (error.status === 401 || error.status === 403) {
      return {
        type: ErrorType.AUTHENTICATION,
        message: 'Authentication failed',
        userMessage: 'Authentication required. Please log in again.',
        code: 'AUTH_ERROR',
        recoverable: true,
        retryable: false,
        timestamp
      };
    }

    // Generation errors
    if (error.type === 'GENERATION_ERROR' || context.action === 'generate') {
      return {
        type: ErrorType.GENERATION,
        message: error.message || 'Generation failed',
        userMessage: 'Failed to generate response. Please try rephrasing your message.',
        code: error.code,
        recoverable: true,
        retryable: true,
        timestamp
      };
    }

    // Validation errors
    if (error.type === 'VALIDATION_ERROR') {
      return {
        type: ErrorType.VALIDATION,
        message: error.message,
        userMessage: error.userMessage || 'Invalid input. Please check your message.',
        code: 'VALIDATION_ERROR',
        recoverable: true,
        retryable: false,
        timestamp
      };
    }

    // Unknown errors
    return {
      type: ErrorType.UNKNOWN,
      message: error.message || 'An unexpected error occurred',
      userMessage: 'Something went wrong. Please try again.',
      code: 'UNKNOWN_ERROR',
      recoverable: true,
      retryable: true,
      timestamp
    };
  }

  onError(listener: (error: AppError, context: ErrorContext) => void): () => void {
    this.errorListeners.push(listener);
    return () => {
      const index = this.errorListeners.indexOf(listener);
      if (index > -1) {
        this.errorListeners.splice(index, 1);
      }
    };
  }

  getRecoveryOptions(error: AppError, context: ErrorContext): RecoveryOption[] {
    const options: RecoveryOption[] = [];

    if (error.retryable) {
      options.push({
        label: 'Try Again',
        action: () => this.retry(context),
        primary: true
      });
    }

    if (error.type === ErrorType.NETWORK) {
      options.push({
        label: 'Check Connection',
        action: () => this.checkConnection()
      });
    }

    if (error.type === ErrorType.AUTHENTICATION) {
      options.push({
        label: 'Log In',
        action: () => this.redirectToLogin(),
        primary: true
      });
    }

    if (error.type === ErrorType.VALIDATION) {
      options.push({
        label: 'Clear Input',
        action: () => this.clearInput(context)
      });
    }

    options.push({
      label: 'Dismiss',
      action: () => {} // No-op, just dismiss
    });

    return options;
  }

  private async retry(context: ErrorContext): Promise<void> {
    // Emit retry event that components can listen to
    window.dispatchEvent(new CustomEvent('error-retry', { detail: context }));
  }

  private async checkConnection(): Promise<void> {
    try {
      await fetch('/api/health', { method: 'HEAD' });
      alert('Connection is working. Please try again.');
    } catch {
      alert('Connection issue detected. Please check your internet connection.');
    }
  }

  private redirectToLogin(): void {
    window.location.href = '/login';
  }

  private clearInput(context: ErrorContext): void {
    window.dispatchEvent(new CustomEvent('clear-input', { detail: context }));
  }
}