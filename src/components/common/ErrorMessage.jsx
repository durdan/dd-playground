import React from 'react';
import './ErrorMessage.css';

export const ErrorMessage = ({ message, onRetry }) => (
  <div className="error-container">
    <div className="error-icon">⚠️</div>
    <div className="error-message">{message}</div>
    {onRetry && (
      <button onClick={onRetry} className="retry-btn">
        Try Again
      </button>
    )}
  </div>
);