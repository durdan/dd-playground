import React, { useEffect, useRef } from 'react';
import { MessageItem } from './MessageItem';
import { TypingIndicator } from './TypingIndicator';
import { useChatState } from './ChatStateContext';
import { ChatMessage } from '../types';

interface MessageListProps {
  messages: ChatMessage[];
  isTyping: boolean;
  projectId: string;
}

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  isTyping,
  projectId
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { state } = useChatState();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  if (messages.length === 0) {
    return (
      <div className="message-list message-list--empty">
        <div className="empty-state">
          <h3>Start a conversation</h3>
          <p>Describe your project requirements and I'll help you create a detailed specification.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="message-list">
      <div className="messages-container">
        {messages.map((message) => (
          <MessageItem
            key={message.id}
            message={message}
            projectId={projectId}
          />
        ))}
        
        {isTyping && <TypingIndicator />}
        
        <div ref={messagesEndRef} />
      </div>
      
      {state.error && (
        <div className="message-error">
          <span className="error-icon">⚠️</span>
          {state.error}
        </div>
      )}
    </div>
  );
};