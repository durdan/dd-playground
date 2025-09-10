import React from 'react';
import './TypingIndicator.css';

interface TypingIndicatorProps {
  isVisible: boolean;
}

export const TypingIndicator: React.FC<TypingIndicatorProps> = ({ isVisible }) => {
  if (!isVisible) return null;

  return (
    <div 
      className="typing-indicator"
      role="status"
      aria-label="Assistant is typing"
      aria-live="polite"
    >
      <div className="typing-indicator__content">
        <div className="typing-indicator__dot"></div>
        <div className="typing-indicator__dot"></div>
        <div className="typing-indicator__dot"></div>
      </div>
    </div>
  );
};