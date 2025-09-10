import React, { useEffect, useState } from 'react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { chatService } from './ChatService';
import { chatStore } from './ChatStore';
import { ChatState, ChatMessage } from './types';
import './ChatContainer.css';

export const ChatContainer: React.FC = () => {
  const [state, setState] = useState<ChatState>(chatStore.getState());

  useEffect(() => {
    const unsubscribe = chatStore.subscribe(setState);
    
    // Load initial messages
    loadMessages();
    
    return unsubscribe;
  }, []);

  const loadMessages = async (): Promise<void> => {
    try {
      chatStore.setLoading(true);
      chatStore.setError(null);
      const messages = await chatService.getMessages();
      messages.forEach(message => chatStore.addMessage(message));
    } catch (error) {
      chatStore.setError(error instanceof Error ? error.message : 'Failed to load messages');
    } finally {
      chatStore.setLoading(false);
    }
  };

  const handleSendMessage = async (content: string): Promise<void> => {
    // Add user message immediately
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      content,
      timestamp: new Date(),
      sender: 'user',
      status: 'sending',
    };
    
    chatStore.addMessage(userMessage);
    chatStore.setLoading(true);
    chatStore.setError(null);

    try {
      // Send message and get response
      const response = await chatService.sendMessage(content);
      
      // Update user message status
      chatStore.updateMessage(userMessage.id, { status: 'sent' });
      
      // Add assistant response
      chatStore.addMessage(response);
    } catch (error) {
      chatStore.updateMessage(userMessage.id, { status: 'error' });
      chatStore.setError(error instanceof Error ? error.message : 'Failed to send message');
    } finally {
      chatStore.setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-container__header">
        <h2>Chat Assistant</h2>
        {state.error && (
          <div className="chat-container__error">
            {state.error}
          </div>
        )}
      </div>
      
      <MessageList 
        messages={state.messages} 
        isLoading={state.isLoading} 
      />
      
      <MessageInput 
        onSendMessage={handleSendMessage}
        disabled={state.isLoading}
      />
    </div>
  );
};