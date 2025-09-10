import React, { useEffect, useRef } from 'react';
import { Message } from './Message';
import { ChatMessage } from './types';
import './MessageList.css';

interface MessageListProps {
  messages: ChatMessage[];
  isLoading?: boolean;
}

export const MessageList: React.FC<MessageListProps> = ({ messages, isLoading = false }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = (): void => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="message-list">
      <div className="message-list__content">
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
        {isLoading && (
          <div className="message-list__loading">
            <div className="loading-indicator">Assistant is typing...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};