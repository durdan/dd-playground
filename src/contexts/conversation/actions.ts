import { ConversationAction, Message, SpecGenerationProgress, UserPreferences } from './types';

export const conversationActions = {
  addMessage: (payload: Omit<Message, 'id' | 'timestamp'>): ConversationAction => ({
    type: 'ADD_MESSAGE',
    payload,
  }),

  updateMessage: (id: string, updates: Partial<Message>): ConversationAction => ({
    type: 'UPDATE_MESSAGE',
    payload: { id, updates },
  }),

  clearMessages: (): ConversationAction => ({
    type: 'CLEAR_MESSAGES',
  }),

  setLoading: (isLoading: boolean): ConversationAction => ({
    type: 'SET_LOADING',
    payload: isLoading,
  }),

  setError: (error: string | null): ConversationAction => ({
    type: 'SET_ERROR',
    payload: error,
  }),

  updateSpecProgress: (progress: SpecGenerationProgress): ConversationAction => ({
    type: 'UPDATE_SPEC_PROGRESS',
    payload: progress,
  }),

  clearSpecProgress: (): ConversationAction => ({
    type: 'CLEAR_SPEC_PROGRESS',
  }),

  updatePreferences: (preferences: Partial<UserPreferences>): ConversationAction => ({
    type: 'UPDATE_PREFERENCES',
    payload: preferences,
  }),

  loadPersistedState: (state: Partial<ConversationAction>): ConversationAction => ({
    type: 'LOAD_PERSISTED_STATE',
    payload: state,
  }),
};