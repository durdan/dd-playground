import React, { useEffect, useRef } from 'react';
import { Message } from '../../types/chat';
import { MessageBubble } from '../MessageBubble/MessageBubble';
import styles from './MessageList.module.css';

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
}

export const MessageList: React.FC<MessageListProps> = ({ messages, isLoading }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className={styles.messageList}>
      {messages.length === 0 ? (
        <div className={styles.emptyState}>
          <p>Start a conversation...</p>
        </div>
      ) : (
        messages.map(message => (
          <MessageBubble key={message.id} message={message} />
        ))
      )}
      
      {isLoading && (
        <div className={styles.loadingIndicator}>
          <div className={styles.typingDots}>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
};