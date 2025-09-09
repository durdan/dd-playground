import React from 'react';
import { MessageBase } from './MessageBase';
import { UserMessage as UserMessageType } from './types';
import { User } from 'lucide-react';

interface UserMessageProps {
  message: UserMessageType;
}

export const UserMessage: React.FC<UserMessageProps> = ({ message }) => {
  return (
    <MessageBase 
      variant="user" 
      timestamp={message.timestamp}
      role="article"
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0">
          {message.avatar ? (
            <img
              src={message.avatar}
              alt="User avatar"
              className="w-8 h-8 rounded-full"
            />
          ) : (
            <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
              <User className="w-4 h-4 text-white" aria-hidden="true" />
            </div>
          )}
        </div>
        <div className="flex-1 min-w-0">
          <div className="text-sm font-medium text-blue-900 mb-1">
            You
          </div>
          <div className="text-gray-800 whitespace-pre-wrap break-words">
            {message.content}
          </div>
        </div>
      </div>
    </MessageBase>
  );
};