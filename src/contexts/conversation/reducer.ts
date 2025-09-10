import { ConversationState, ConversationAction, Message } from './types';

const generateId = (): string => `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

const createMessage = (payload: Omit<Message, 'id' | 'timestamp'>): Message => ({
  ...payload,
  id: generateId(),
  timestamp: new Date(),
});

const trimMessages = (messages: Message[], maxSize: number): Message[] => {
  if (messages.length <= maxSize) return messages;
  
  // Keep system messages and trim from the middle, preserving recent messages
  const systemMessages = messages.filter(msg => msg.role === 'system');
  const nonSystemMessages = messages.filter(msg => msg.role !== 'system');
  
  if (nonSystemMessages.length <= maxSize - systemMessages.length) {
    return messages;
  }
  
  const keepRecent = Math.floor((maxSize - systemMessages.length) / 2);
  const keepOld = maxSize - systemMessages.length - keepRecent;
  
  return [
    ...systemMessages,
    ...nonSystemMessages.slice(0, keepOld),
    ...nonSystemMessages.slice(-keepRecent),
  ].sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime());
};

export const conversationReducer = (
  state: ConversationState,
  action: ConversationAction
): ConversationState => {
  switch (action.type) {
    case 'ADD_MESSAGE': {
      const newMessage = createMessage(action.payload);
      const updatedMessages = [...state.messages, newMessage];
      const trimmedMessages = trimMessages(updatedMessages, state.userPreferences.maxHistorySize);
      
      return {
        ...state,
        messages: trimmedMessages,
        error: null,
      };
    }

    case 'UPDATE_MESSAGE': {
      const messages = state.messages.map(msg =>
        msg.id === action.payload.id
          ? { ...msg, ...action.payload.updates }
          : msg
      );
      
      return { ...state, messages };
    }

    case 'CLEAR_MESSAGES':
      return {
        ...state,
        messages: [],
        error: null,
      };

    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      };

    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        isLoading: false,
      };

    case 'UPDATE_SPEC_PROGRESS':
      return {
        ...state,
        currentSpecProgress: action.payload,
      };

    case 'CLEAR_SPEC_PROGRESS':
      return {
        ...state,
        currentSpecProgress: null,
      };

    case 'UPDATE_PREFERENCES': {
      const updatedPreferences = {
        ...state.userPreferences,
        ...action.payload,
      };
      
      // If maxHistorySize changed, trim messages accordingly
      const messages = action.payload.maxHistorySize
        ? trimMessages(state.messages, action.payload.maxHistorySize)
        : state.messages;
      
      return {
        ...state,
        userPreferences: updatedPreferences,
        messages,
      };
    }

    case 'LOAD_PERSISTED_STATE':
      return {
        ...state,
        ...action.payload,
      };

    default:
      return state;
  }
};