import React from 'react';
import { Message } from '../types/chat';
import './MessageBubble.css';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const formatTime = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`message-bubble ${message.sender}`}>
      <div className="message-content">
        {message.content}
      </div>
      <div className="message-meta">
        <span className="message-time">{formatTime(message.timestamp)}</span>
        {message.status === 'sending' && <span className="message-status">Sending...</span>}
        {message.status === 'error' && <span className="message-status error">Failed</span>}
      </div>
    </div>
  );
};