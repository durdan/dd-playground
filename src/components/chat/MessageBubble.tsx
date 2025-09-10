import React from 'react';
import { ChatMessage } from './types';
import './MessageBubble.css';

interface MessageBubbleProps {
  message: ChatMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';
  
  return (
    <div 
      className={`message-bubble ${isUser ? 'message-bubble--user' : 'message-bubble--assistant'}`}
      role="article"
      aria-label={`Message from ${isUser ? 'you' : 'assistant'}`}
    >
      <div className="message-bubble__content">
        {message.content}
      </div>
      <div className="message-bubble__timestamp">
        {message.timestamp.toLocaleTimeString([], { 
          hour: '2-digit', 
          minute: '2-digit' 
        })}
      </div>
      {message.specType && (
        <div className="message-bubble__spec-type">
          {message.specType}
        </div>
      )}
    </div>
  );
};