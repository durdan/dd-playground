export enum ErrorSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical',
}

export enum ErrorCategory {
  VALIDATION = 'validation',
  NETWORK = 'network',
  DATABASE = 'database',
  AUTHENTICATION = 'authentication',
  AUTHORIZATION = 'authorization',
  BUSINESS_LOGIC = 'business_logic',
  SYSTEM = 'system',
  EXTERNAL_SERVICE = 'external_service',
  CONFIGURATION = 'configuration',
  USER_INPUT = 'user_input',
}

export enum RecoveryAction {
  RETRY = 'retry',
  FALLBACK = 'fallback',
  IGNORE = 'ignore',
  ESCALATE = 'escalate',
  AUTO_FIX = 'auto_fix',
  USER_INTERVENTION = 'user_intervention',
  GRACEFUL_DEGRADATION = 'graceful_degradation',
}

export interface ErrorContext {
  timestamp: Date;
  userId?: string;
  sessionId?: string;
  requestId?: string;
  userAgent?: string;
  ip?: string;
  route?: string;
  method?: string;
  params?: Record<string, any>;
  body?: Record<string, any>;
  headers?: Record<string, string>;
  stackTrace?: string;
  metadata?: Record<string, any>;
}

export interface ErrorSuggestion {
  id: string;
  message: string;
  action?: string;
  priority: number;
  category: 'user' | 'developer' | 'system';
}

export interface RecoveryStrategy {
  action: RecoveryAction;
  priority: number;
  condition?: (error: ClassifiedError) => boolean;
  execute: (error: ClassifiedError) => Promise<RecoveryResult>;
  maxAttempts?: number;
  backoffMs?: number;
}

export interface RecoveryResult {
  success: boolean;
  message?: string;
  data?: any;
  shouldRetry?: boolean;
  nextStrategy?: RecoveryAction;
}

export interface AutoFixResult {
  applied: boolean;
  description: string;
  confidence: number;
  rollbackInfo?: any;
}

export interface ClassifiedError {
  id: string;
  originalError: Error;
  message: string;
  code?: string;
  severity: ErrorSeverity;
  category: ErrorCategory;
  context: ErrorContext;
  suggestions: ErrorSuggestion[];
  recoveryStrategies: RecoveryStrategy[];
  isRecoverable: boolean;
  canAutoFix: boolean;
  tags: string[];
  fingerprint: string;
}

export interface ErrorHandlerConfig {
  enableAutoFix: boolean;
  enableAutoRetry: boolean;
  maxRetryAttempts: number;
  retryDelayMs: number;
  enableLogging: boolean;
  enableTelemetry: boolean;
  severityThreshold: ErrorSeverity;
}

export interface ErrorPattern {
  name: string;
  pattern: RegExp | ((error: Error) => boolean);
  category: ErrorCategory;
  severity: ErrorSeverity;
  suggestions: Omit<ErrorSuggestion, 'id'>[];
  recoveryStrategies: Omit<RecoveryStrategy, 'execute'>[];
  autoFixable: boolean;
  tags: string[];
}