import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { ChatMessage, Specification, ChatState, ChatAction } from '../types';

interface ChatStateContextType {
  state: ChatState;
  dispatch: React.Dispatch<ChatAction>;
  addMessage: (message: ChatMessage) => void;
  updateSpecification: (spec: Partial<Specification>) => void;
  setTyping: (isTyping: boolean) => void;
  clearMessages: () => void;
}

const ChatStateContext = createContext<ChatStateContextType | null>(null);

const chatReducer = (state: ChatState, action: ChatAction): ChatState => {
  switch (action.type) {
    case 'ADD_MESSAGE':
      return {
        ...state,
        messages: [...state.messages, action.payload],
        lastActivity: new Date()
      };
    
    case 'UPDATE_SPECIFICATION':
      return {
        ...state,
        specification: state.specification 
          ? { ...state.specification, ...action.payload }
          : action.payload as Specification,
        lastSpecUpdate: new Date()
      };
    
    case 'SET_TYPING':
      return {
        ...state,
        isTyping: action.payload
      };
    
    case 'CLEAR_MESSAGES':
      return {
        ...state,
        messages: [],
        lastActivity: new Date()
      };
    
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload
      };
    
    default:
      return state;
  }
};

interface ChatStateProviderProps {
  children: ReactNode;
  projectId: string;
  initialMessages?: ChatMessage[];
  specification?: Specification;
}

export const ChatStateProvider: React.FC<ChatStateProviderProps> = ({
  children,
  projectId,
  initialMessages = [],
  specification
}) => {
  const [state, dispatch] = useReducer(chatReducer, {
    projectId,
    messages: initialMessages,
    specification,
    isTyping: false,
    lastActivity: new Date(),
    error: null
  });

  const addMessage = (message: ChatMessage) => {
    dispatch({ type: 'ADD_MESSAGE', payload: message });
  };

  const updateSpecification = (spec: Partial<Specification>) => {
    dispatch({ type: 'UPDATE_SPECIFICATION', payload: spec });
  };

  const setTyping = (isTyping: boolean) => {
    dispatch({ type: 'SET_TYPING', payload: isTyping });
  };

  const clearMessages = () => {
    dispatch({ type: 'CLEAR_MESSAGES' });
  };

  return (
    <ChatStateContext.Provider value={{
      state,
      dispatch,
      addMessage,
      updateSpecification,
      setTyping,
      clearMessages
    }}>
      {children}
    </ChatStateContext.Provider>
  );
};

export const useChatState = (): ChatStateContextType => {
  const context = useContext(ChatStateContext);
  if (!context) {
    throw new Error('useChatState must be used within ChatStateProvider');
  }
  return context;
};