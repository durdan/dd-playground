import React, { useState, useEffect, useCallback } from 'react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { LoadingIndicator } from './LoadingIndicator';
import { websocketService, WebSocketMessage, SpecGenerationProgress } from '../services/websocketService';
import { apiService, ChatMessage } from '../services/apiService';

export const ChatUI: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [progress, setProgress] = useState<SpecGenerationProgress | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleWebSocketMessage = useCallback((wsMessage: WebSocketMessage) => {
    switch (wsMessage.type) {
      case 'spec_generation_start':
        setIsGenerating(true);
        setProgress({ stage: 'Starting', progress: 0, message: 'Initializing specification generation...' });
        break;

      case 'spec_generation_progress':
        setProgress(wsMessage.data as SpecGenerationProgress);
        break;

      case 'spec_generation_complete':
        setIsGenerating(false);
        setProgress(null);
        const newSpecMessage: ChatMessage = {
          id: Date.now().toString(),
          content: '',
          timestamp: new Date(),
          type: 'spec',
          specData: wsMessage.data
        };
        setMessages(prev => [...prev, newSpecMessage]);
        break;

      case 'error':
        setIsGenerating(false);
        setProgress(null);
        setError(wsMessage.data.message || 'An error occurred');
        break;
    }
  }, []);

  useEffect(() => {
    const initializeConnection = async () => {
      try {
        await websocketService.connect('ws://localhost:3001');
        const unsubscribe = websocketService.subscribe('all', handleWebSocketMessage);
        
        // Load chat history
        const history = await apiService.getChatHistory();
        setMessages(history);

        return unsubscribe;
      } catch (error) {
        console.error('Failed to initialize connection:', error);
        setError('Failed to connect to server');
      }
    };

    const cleanup = initializeConnection();
    
    return () => {
      cleanup.then(unsubscribe => unsubscribe?.());
      websocketService.disconnect();
    };
  }, [handleWebSocketMessage]);

  const handleSendMessage = async (messageContent: string) => {
    if (isGenerating) return;

    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: messageContent,
      timestamp: new Date(),
      type: 'user'
    };
    setMessages(prev => [...prev, userMessage]);
    setError(null);

    try {
      // Start specification generation
      await apiService.generateSpecification({
        message: messageContent,
        context: messages.slice(-5).map(m => m.content) // Last 5 messages for context
      });
    } catch (error) {
      console.error('Failed to generate specification:', error);
      setError('Failed to generate specification. Please try again.');
    }
  };

  return (
    <div className="chat-ui">
      <div className="chat-header">
        <h1>Specification Generator</h1>
        {error && <div className="error-message">{error}</div>}
      </div>
      
      <div className="chat-content">
        <MessageList messages={messages} />
        <LoadingIndicator progress={progress} isVisible={isGenerating} />
      </div>
      
      <div className="chat-input">
        <MessageInput onSendMessage={handleSendMessage} disabled={isGenerating} />
      </div>
    </div>
  );
};