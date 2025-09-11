import React from 'react';
import './LoadingSpinner.css';

export const LoadingSpinner = () => (
  <div className="loading-container">
    <div className="loading-spinner"></div>
    <div className="loading-text">Loading dashboard...</div>
  </div>
);