import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react';
import { ConversationState, ConversationAction, UserPreferences } from './types';
import { conversationReducer } from './reducer';
import { conversationActions } from './actions';
import { conversationSelectors } from './selectors';
import { storage } from './storage';

const defaultPreferences: UserPreferences = {
  theme: 'system',
  language: 'en',
  autoSave: true,
  maxHistorySize: 100,
  notifications: {
    specComplete: true,
    errors: true,
  },
};

const initialState: ConversationState = {
  messages: [],
  currentSpecProgress: null,
  userPreferences: defaultPreferences,
  isLoading: false,
  error: null,
};

interface ConversationContextValue {
  state: ConversationState;
  dispatch: React.Dispatch<ConversationAction>;
  actions: typeof conversationActions;
  selectors: typeof conversationSelectors;
}

const ConversationContext = createContext<ConversationContextValue | null>(null);

interface ConversationProviderProps {
  children: ReactNode;
}

export const ConversationProvider: React.FC<ConversationProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(conversationReducer, initialState);

  // Load persisted state on mount
  useEffect(() => {
    const loadPersistedData = async () => {
      try {
        const preferences = storage.loadPreferences();
        const messages = storage.loadMessages();

        if (preferences || messages.length > 0) {
          dispatch(conversationActions.loadPersistedState({
            userPreferences: preferences || defaultPreferences,
            messages: messages,
          }));
        }
      } catch (error) {
        console.warn('Failed to load persisted state:', error);
      }
    };

    loadPersistedData();
  }, []);

  // Auto-save preferences when they change
  useEffect(() => {
    if (state.userPreferences.autoSave) {
      storage.savePreferences(state.userPreferences);
    }
  }, [state.userPreferences]);

  // Auto-save messages when they change (debounced)
  useEffect(() => {
    if (state.userPreferences.autoSave && state.messages.length > 0) {
      const timeoutId = setTimeout(() => {
        storage.saveMessages(state.messages);
      }, 1000); // Debounce saves

      return () => clearTimeout(timeoutId);
    }
  }, [state.messages, state.userPreferences.autoSave]);

  const contextValue: ConversationContextValue = {
    state,
    dispatch,
    actions: conversationActions,
    selectors: conversationSelectors,
  };

  return (
    <ConversationContext.Provider value={contextValue}>
      {children}
    </ConversationContext.Provider>
  );
};

export const useConversation = (): ConversationContextValue => {
  const context = useContext(ConversationContext);
  if (!context) {
    throw new Error('useConversation must be used within a ConversationProvider');
  }
  return context;
};