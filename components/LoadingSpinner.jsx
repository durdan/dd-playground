import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = ({ size = 'medium', overlay = false, message = 'Loading...' }) => {
  const sizeClasses = {
    small: 'spinner-small',
    medium: 'spinner-medium',
    large: 'spinner-large'
  };

  const spinner = (
    <div className={`loading-spinner ${sizeClasses[size]}`}>
      <div className="spinner-circle"></div>
      {message && <p className="spinner-message">{message}</p>}
    </div>
  );

  if (overlay) {
    return (
      <div className="spinner-overlay">
        {spinner}
      </div>
    );
  }

  return spinner;
};

export default LoadingSpinner;