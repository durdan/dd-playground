import React, { useEffect, useRef } from 'react';
import { MessageItem } from './MessageItem';
import { TypingIndicator } from './TypingIndicator';
import { useChatState } from './ChatStateContext';
import { ChatMessage, Specification } from '../types';

interface MessageListProps {
  messages: ChatMessage[];
  isTyping: boolean;
  onSpecificationUpdate: (spec: Partial<Specification>) => void;
}

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  isTyping,
  onSpecificationUpdate
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { state } = useChatState();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSpecificationExtract = (message: ChatMessage) => {
    if (message.specificationUpdate) {
      onSpecificationUpdate(message.specificationUpdate);
    }
  };

  return (
    <div className="message-list">
      <div className="messages-container">
        {messages.length === 0 && (
          <div className="empty-state">
            <h3>Start describing your project requirements</h3>
            <p>I'll help you create a comprehensive specification document.</p>
          </div>
        )}
        
        {messages.map((message) => (
          <MessageItem
            key={message.id}
            message={message}
            onSpecificationExtract={handleSpecificationExtract}
          />
        ))}
        
        {isTyping && <TypingIndicator />}
        
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};