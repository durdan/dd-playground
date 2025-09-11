import { useState, useCallback } from 'react';
import { Message, SpecType, ChatState } from '../types/chat';

export const useChat = () => {
  const [state, setState] = useState<ChatState>({
    messages: [],
    currentSpecType: 'general',
    isLoading: false
  });

  const addMessage = useCallback((content: string, sender: 'user' | 'assistant') => {
    if (!content.trim()) {
      throw new Error('Message content cannot be empty');
    }

    const newMessage: Message = {
      id: Date.now().toString(),
      content: content.trim(),
      sender,
      timestamp: new Date(),
      specType: state.currentSpecType
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, newMessage]
    }));
  }, [state.currentSpecType]);

  const setSpecType = useCallback((specType: SpecType) => {
    setState(prev => ({ ...prev, currentSpecType: specType }));
  }, []);

  const setLoading = useCallback((isLoading: boolean) => {
    setState(prev => ({ ...prev, isLoading }));
  }, []);

  return {
    ...state,
    addMessage,
    setSpecType,
    setLoading
  };
};