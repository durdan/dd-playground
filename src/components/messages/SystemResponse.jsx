import React, { useState, useEffect } from 'react';
import MessageBase from './MessageBase';
import './SystemResponse.css';

const SystemResponse = ({ 
  message, 
  timestamp, 
  status = 'completed', // 'typing', 'processing', 'completed', 'error'
  systemName = 'Assistant',
  showTypingEffect = false
}) => {
  const [displayedMessage, setDisplayedMessage] = useState('');
  const [isTyping, setIsTyping] = useState(showTypingEffect && status === 'completed');

  useEffect(() => {
    if (showTypingEffect && message && status === 'completed') {
      setIsTyping(true);
      let index = 0;
      const timer = setInterval(() => {
        if (index < message.length) {
          setDisplayedMessage(message.slice(0, index + 1));
          index++;
        } else {
          setIsTyping(false);
          clearInterval(timer);
        }
      }, 30);
      return () => clearInterval(timer);
    } else {
      setDisplayedMessage(message || '');
    }
  }, [message, showTypingEffect, status]);

  const getStatusIcon = () => {
    switch (status) {
      case 'typing': return '✏️';
      case 'processing': return '⚙️';
      case 'error': return '❌';
      default: return '🤖';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'typing': return 'Typing...';
      case 'processing': return 'Processing...';
      case 'error': return 'Error occurred';
      default: return '';
    }
  };

  return (
    <MessageBase type="system" timestamp={timestamp}>
      <div className={`system-response status-${status}`}>
        <div className="system-header">
          <span className="system-icon">{getStatusIcon()}</span>
          <span className="system-name">{systemName}</span>
          {status !== 'completed' && (
            <span className="system-status">{getStatusText()}</span>
          )}
        </div>
        <div className="system-content">
          {displayedMessage}
          {isTyping && <span className="typing-cursor">|</span>}
        </div>
      </div>
    </MessageBase>
  );
};

export default SystemResponse;