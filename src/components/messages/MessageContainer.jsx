import React from 'react';
import UserMessage from './UserMessage';
import SystemResponse from './SystemResponse';
import SpecPreview from './SpecPreview';
import InteractiveSpecCustomizer from './InteractiveSpecCustomizer';

const MessageContainer = ({ message }) => {
  if (!message || !message.type) {
    throw new Error('Message with valid type is required');
  }

  const { type, timestamp = new Date(), ...props } = message;

  switch (type) {
    case 'user':
      return <UserMessage timestamp={timestamp} {...props} />;
    
    case 'system':
      return <SystemResponse timestamp={timestamp} {...props} />;
    
    case 'spec-preview':
      return <SpecPreview timestamp={timestamp} {...props} />;
    
    case 'interactive':
      return <InteractiveSpecCustomizer timestamp={timestamp} {...props} />;
    
    default:
      throw new Error(`Unknown message type: ${type}`);
  }
};

export default MessageContainer;