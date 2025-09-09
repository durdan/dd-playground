import { useState, useCallback } from 'react';
import { Message, ChatState } from '../types/chat';

export const useChatState = () => {
  const [state, setState] = useState<ChatState>({
    messages: [],
    isLoading: false
  });

  const addMessage = useCallback((content: string, sender: 'user' | 'assistant') => {
    const newMessage: Message = {
      id: Date.now().toString(),
      content: content.trim(),
      sender,
      timestamp: new Date()
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, newMessage]
    }));
  }, []);

  const setLoading = useCallback((loading: boolean) => {
    setState(prev => ({ ...prev, isLoading: loading }));
  }, []);

  const clearMessages = useCallback(() => {
    setState({ messages: [], isLoading: false });
  }, []);

  return {
    ...state,
    addMessage,
    setLoading,
    clearMessages
  };
};