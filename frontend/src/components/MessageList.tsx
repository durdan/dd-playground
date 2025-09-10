import React from 'react';
import { ChatMessage } from '../services/apiService';

interface MessageListProps {
  messages: ChatMessage[];
}

export const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div className="message-list">
      {messages.map((message) => (
        <div key={message.id} className={`message ${message.type}`}>
          <div className="message-content">
            {message.type === 'spec' && message.specData ? (
              <div className="spec-message">
                <h3>{message.specData.title}</h3>
                <pre className="spec-content">{message.specData.content}</pre>
              </div>
            ) : (
              <p>{message.content}</p>
            )}
          </div>
          <div className="message-timestamp">
            {new Date(message.timestamp).toLocaleTimeString()}
          </div>
        </div>
      ))}
    </div>
  );
};