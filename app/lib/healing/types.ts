export interface ErrorPattern {
  id: string;
  name: string;
  description: string;
  errorRegex: RegExp;
  contextPatterns?: string[];
  category: ErrorCategory;
  severity: ErrorSeverity;
  fixes: Fix[];
  metadata: {
    frequency: number;
    successRate: number;
    lastUpdated: Date;
    createdBy: string;
  };
}

export interface Fix {
  id: string;
  name: string;
  description: string;
  type: FixType;
  confidence: number;
  action: FixAction;
  preconditions?: string[];
  rollbackAction?: FixAction;
  estimatedTime: number;
  riskLevel: RiskLevel;
}

export interface FixAction {
  type: 'replace' | 'insert' | 'delete' | 'transform' | 'validate';
  target?: string;
  content?: string;
  position?: number;
  transform?: (input: string) => string;
}

export interface HealingAttempt {
  id: string;
  timestamp: Date;
  errorPattern: ErrorPattern;
  appliedFix: Fix;
  originalContent: string;
  fixedContent: string;
  success: boolean;
  confidence: number;
  userFeedback?: UserFeedback;
  context: HealingContext;
}

export interface UserFeedback {
  rating: number;
  accepted: boolean;
  improvementSuggestion?: string;
  timestamp: Date;
}

export interface HealingContext {
  errorMessage: string;
  stackTrace?: string;
  codeContext: string;
  lineNumber?: number;
  fileName?: string;
  userAction?: string;
  environment: {
    browser?: string;
    version?: string;
    platform?: string;
  };
}

export interface LearningData {
  patternId: string;
  fixId: string;
  success: boolean;
  userAccepted: boolean;
  context: HealingContext;
  timestamp: Date;
}

export interface ConfidenceScore {
  overall: number;
  patternMatch: number;
  fixReliability: number;
  contextSimilarity: number;
  historicalSuccess: number;
}

export enum ErrorCategory {
  SYNTAX = 'syntax',
  SEMANTIC = 'semantic',
  RUNTIME = 'runtime',
  VALIDATION = 'validation',
  PERFORMANCE = 'performance',
  SECURITY = 'security'
}

export enum ErrorSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export enum FixType {
  AUTOMATIC = 'automatic',
  SUGGESTED = 'suggested',
  MANUAL = 'manual'
}

export enum RiskLevel {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high'
}

export interface HealingResult {
  success: boolean;
  appliedFixes: Fix[];
  originalContent: string;
  healedContent: string;
  confidence: ConfidenceScore;
  suggestions: string[];
  warnings: string[];
  metadata: {
    processingTime: number;
    patternsMatched: number;
    fixesAttempted: number;
  };
}

export interface HealingOptions {
  autoApply: boolean;
  confidenceThreshold: number;
  maxAttempts: number;
  riskTolerance: RiskLevel;
  learningEnabled: boolean;
  categories: ErrorCategory[];
}