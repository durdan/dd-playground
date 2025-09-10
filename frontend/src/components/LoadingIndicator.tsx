import React from 'react';
import { SpecGenerationProgress } from '../services/websocketService';

interface LoadingIndicatorProps {
  progress: SpecGenerationProgress | null;
  isVisible: boolean;
}

export const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({ progress, isVisible }) => {
  if (!isVisible) return null;

  return (
    <div className="loading-indicator">
      <div className="loading-content">
        <div className="spinner"></div>
        <div className="progress-info">
          <div className="stage">{progress?.stage || 'Initializing...'}</div>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${progress?.progress || 0}%` }}
            ></div>
          </div>
          <div className="message">{progress?.message || 'Starting generation...'}</div>
        </div>
      </div>
    </div>
  );
};