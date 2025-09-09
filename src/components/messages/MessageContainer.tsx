import React from 'react';
import { Message } from './types';
import { UserMessage } from './UserMessage';
import { SystemMessage } from './SystemMessage';
import { SpecPreview } from './SpecPreview';
import { LoadingMessage } from './LoadingMessage';

interface MessageContainerProps {
  messages: Message[];
  className?: string;
}

export const MessageContainer: React.FC<MessageContainerProps> = ({ 
  messages, 
  className = '' 
}) => {
  const renderMessage = (message: Message) => {
    switch (message.type) {
      case 'user':
        return <UserMessage key={message.id} message={message} />;
      case 'system':
        return <SystemMessage key={message.id} message={message} />;
      case 'spec':
        return <SpecPreview key={message.id} message={message} />;
      case 'loading':
        return <LoadingMessage key={message.id} message={message} />;
      default:
        return null;
    }
  };

  return (
    <div 
      className={`flex flex-col gap-4 p-4 ${className}`}
      role="log"
      aria-label="Conversation messages"
    >
      {messages.map(renderMessage)}
    </div>
  );
};