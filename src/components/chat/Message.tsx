import React from 'react';
import { ChatMessage } from './types';
import './Message.css';

interface MessageProps {
  message: ChatMessage;
}

export const Message: React.FC<MessageProps> = ({ message }) => {
  const formatTime = (timestamp: Date): string => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`message message--${message.sender}`}>
      <div className="message__content">
        {message.content}
      </div>
      <div className="message__meta">
        <span className="message__time">{formatTime(message.timestamp)}</span>
        {message.status && (
          <span className={`message__status message__status--${message.status}`}>
            {message.status}
          </span>
        )}
      </div>
    </div>
  );
};