export enum ErrorType {
  NETWORK = 'NETWORK',
  GENERATION = 'GENERATION',
  VALIDATION = 'VALIDATION',
  RATE_LIMIT = 'RATE_LIMIT',
  AUTHENTICATION = 'AUTHENTICATION',
  UNKNOWN = 'UNKNOWN'
}

export interface AppError {
  type: ErrorType;
  message: string;
  userMessage: string;
  code?: string;
  details?: any;
  recoverable: boolean;
  retryable: boolean;
  timestamp: Date;
}

export interface RecoveryOption {
  label: string;
  action: () => void | Promise<void>;
  primary?: boolean;
}

export interface ErrorContext {
  component: string;
  action: string;
  userId?: string;
  sessionId?: string;
  metadata?: Record<string, any>;
}