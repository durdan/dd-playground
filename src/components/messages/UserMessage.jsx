import React from 'react';
import MessageBase from './MessageBase';
import './UserMessage.css';

const UserMessage = ({ 
  message, 
  timestamp, 
  userName = 'You',
  avatar 
}) => {
  if (!message?.trim()) {
    throw new Error('User message content is required');
  }

  return (
    <MessageBase type="user" timestamp={timestamp}>
      <div className="user-message">
        <div className="user-header">
          {avatar && <img src={avatar} alt={userName} className="user-avatar" />}
          <span className="user-name">{userName}</span>
        </div>
        <div className="user-content">
          {message}
        </div>
      </div>
    </MessageBase>
  );
};

export default UserMessage;