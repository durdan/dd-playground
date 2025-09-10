import React from 'react';
import { AppError, RecoveryOption } from '../errors/ErrorTypes';

interface ErrorDisplayProps {
  error: AppError;
  recoveryOptions: RecoveryOption[];
  onDismiss: () => void;
}

export const ErrorDisplay: React.FC<ErrorDisplayProps> = ({
  error,
  recoveryOptions,
  onDismiss
}) => {
  const getErrorIcon = () => {
    switch (error.type) {
      case 'NETWORK':
        return '🌐';
      case 'GENERATION':
        return '🤖';
      case 'VALIDATION':
        return '⚠️';
      case 'RATE_LIMIT':
        return '⏱️';
      case 'AUTHENTICATION':
        return '🔒';
      default:
        return '❌';
    }
  };

  const getErrorColor = () => {
    switch (error.type) {
      case 'NETWORK':
        return 'border-blue-500 bg-blue-50';
      case 'VALIDATION':
        return 'border-yellow-500 bg-yellow-50';
      case 'RATE_LIMIT':
        return 'border-orange-500 bg-orange-50';
      case 'AUTHENTICATION':
        return 'border-purple-500 bg-purple-50';
      default:
        return 'border-red-500 bg-red-50';
    }
  };

  return (
    <div className={`border-l-4 p-4 mb-4 rounded ${getErrorColor()}`}>
      <div className="flex items-start">
        <span className="text-2xl mr-3">{getErrorIcon()}</span>
        <div className="flex-1">
          <h3 className="font-semibold text-gray-800 mb-1">
            {error.type.replace('_', ' ')} Error
          </h3>
          <p className="text-gray-700 mb-3">{error.userMessage}</p>
          
          {recoveryOptions.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {recoveryOptions.map((option, index) => (
                <button
                  key={index}
                  onClick={option.action}
                  className={`px-3 py-1 rounded text-sm font-medium ${
                    option.primary
                      ? 'bg-blue-600 text-white hover:bg-blue-700'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {option.label}
                </button>
              ))}
            </div>
          )}
          
          <button
            onClick={onDismiss}
            className="absolute top-2 right-2 text-gray-400 hover:text-gray-600"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  );
};