export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  timestamp: Date;
  metadata?: {
    specId?: string;
    progress?: number;
    error?: string;
  };
}

export interface SpecGenerationProgress {
  specId: string;
  stage: 'analyzing' | 'generating' | 'reviewing' | 'complete' | 'error';
  progress: number; // 0-100
  currentStep?: string;
  error?: string;
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  language: string;
  autoSave: boolean;
  maxHistorySize: number;
  notifications: {
    specComplete: boolean;
    errors: boolean;
  };
}

export interface ConversationState {
  messages: Message[];
  currentSpecProgress: SpecGenerationProgress | null;
  userPreferences: UserPreferences;
  isLoading: boolean;
  error: string | null;
}

export type ConversationAction =
  | { type: 'ADD_MESSAGE'; payload: Omit<Message, 'id' | 'timestamp'> }
  | { type: 'UPDATE_MESSAGE'; payload: { id: string; updates: Partial<Message> } }
  | { type: 'CLEAR_MESSAGES' }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'UPDATE_SPEC_PROGRESS'; payload: SpecGenerationProgress }
  | { type: 'CLEAR_SPEC_PROGRESS' }
  | { type: 'UPDATE_PREFERENCES'; payload: Partial<UserPreferences> }
  | { type: 'LOAD_PERSISTED_STATE'; payload: Partial<ConversationState> };