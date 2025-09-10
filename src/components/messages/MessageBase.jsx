import React from 'react';
import './MessageBase.css';

const MessageBase = ({ 
  type, 
  timestamp, 
  children, 
  className = '',
  showTimestamp = true 
}) => {
  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className={`message-base message-${type} ${className}`}>
      <div className="message-content">
        {children}
      </div>
      {showTimestamp && (
        <div className="message-timestamp">
          {formatTime(timestamp)}
        </div>
      )}
    </div>
  );
};

export default MessageBase;