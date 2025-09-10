import { UserPreferences, ConversationState } from './types';

const STORAGE_KEYS = {
  PREFERENCES: 'conversation_preferences',
  MESSAGES: 'conversation_messages',
} as const;

export const storage = {
  savePreferences: (preferences: UserPreferences): void => {
    try {
      localStorage.setItem(STORAGE_KEYS.PREFERENCES, JSON.stringify(preferences));
    } catch (error) {
      console.warn('Failed to save preferences:', error);
    }
  },

  loadPreferences: (): UserPreferences | null => {
    try {
      const stored = localStorage.getItem(STORAGE_KEYS.PREFERENCES);
      return stored ? JSON.parse(stored) : null;
    } catch (error) {
      console.warn('Failed to load preferences:', error);
      return null;
    }
  },

  saveMessages: (messages: ConversationState['messages']): void => {
    try {
      // Only save recent messages to avoid localStorage size limits
      const recentMessages = messages.slice(-50).map(msg => ({
        ...msg,
        timestamp: msg.timestamp.toISOString(), // Serialize dates
      }));
      localStorage.setItem(STORAGE_KEYS.MESSAGES, JSON.stringify(recentMessages));
    } catch (error) {
      console.warn('Failed to save messages:', error);
    }
  },

  loadMessages: (): ConversationState['messages'] => {
    try {
      const stored = localStorage.getItem(STORAGE_KEYS.MESSAGES);
      if (!stored) return [];
      
      const parsed = JSON.parse(stored);
      return parsed.map((msg: any) => ({
        ...msg,
        timestamp: new Date(msg.timestamp), // Deserialize dates
      }));
    } catch (error) {
      console.warn('Failed to load messages:', error);
      return [];
    }
  },

  clear: (): void => {
    try {
      localStorage.removeItem(STORAGE_KEYS.PREFERENCES);
      localStorage.removeItem(STORAGE_KEYS.MESSAGES);
    } catch (error) {
      console.warn('Failed to clear storage:', error);
    }
  },
};