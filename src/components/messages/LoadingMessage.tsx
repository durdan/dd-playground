import React from 'react';
import { MessageBase } from './MessageBase';
import { LoadingMessage as LoadingMessageType } from './types';
import { Bot, Loader2 } from 'lucide-react';

interface LoadingMessageProps {
  message: LoadingMessageType;
}

export const LoadingMessage: React.FC<LoadingMessageProps> = ({ message }) => {
  return (
    <MessageBase 
      variant="loading"
      role="status"
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center">
            <Bot className="w-4 h-4 text-white" aria-hidden="true" />
          </div>
        </div>
        <div className="flex-1 min-w-0">
          <div className="text-sm font-medium text-yellow-900 mb-1 flex items-center gap-2">
            <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
            Assistant is thinking...
          </div>
          {message.message && (
            <div className="text-gray-700 text-sm">
              {message.message}
            </div>
          )}
        </div>
      </div>
      <div 
        className="sr-only" 
        aria-live="polite" 
        aria-atomic="true"
      >
        Loading response, please wait
      </div>
    </MessageBase>
  );
};