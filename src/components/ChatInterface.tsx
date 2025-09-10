import React, { useState, useCallback } from 'react';
import { Message } from '../types/chat';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { useChatSocket } from '../hooks/useChatSocket';
import { chatService } from '../services/chatService';
import './ChatInterface.css';

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleMessageReceived = useCallback((message: Message) => {
    setMessages(prev => [...prev, message]);
  }, []);

  const { isConnected, sendMessage, isTyping } = useChatSocket(handleMessageReceived);

  const handleSendMessage = async (content: string) => {
    try {
      setError(null);
      
      // Create user message
      const userMessage: Message = {
        id: chatService.generateMessageId(),
        content,
        sender: 'user',
        timestamp: new Date(),
        status: 'sending'
      };

      // Add to local state immediately
      setMessages(prev => [...prev, userMessage]);

      // Send via WebSocket if connected, otherwise use HTTP
      if (isConnected) {
        sendMessage(userMessage);
        // Update status to sent
        setMessages(prev => 
          prev.map(msg => 
            msg.id === userMessage.id 
              ? { ...msg, status: 'sent' }
              : msg
          )
        );
      } else {
        // Fallback to HTTP API
        await chatService.sendMessage(content);
        setMessages(prev => 
          prev.map(msg => 
            msg.id === userMessage.id 
              ? { ...msg, status: 'sent' }
              : msg
          )
        );
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
      // Mark message as failed
      setMessages(prev => 
        prev.map(msg => 
          msg.sender === 'user' && msg.status === 'sending'
            ? { ...msg, status: 'error' }
            : msg
        )
      );
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>Chat Assistant</h2>
        <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
          {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
        </div>
      </div>
      
      {error && (
        <div className="error-banner">
          {error}
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}
      
      <MessageList messages={messages} isTyping={isTyping} />
      
      <MessageInput 
        onSendMessage={handleSendMessage}
        disabled={!isConnected}
        placeholder={isConnected ? "Type your message..." : "Connecting..."}
      />
    </div>
  );
};