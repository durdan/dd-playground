import React from 'react';
import { Message } from '../../types/chat';
import styles from './MessageBubble.module.css';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`${styles.bubble} ${styles[message.sender]}`}>
      <div className={styles.content}>
        {message.content}
      </div>
      <div className={styles.timestamp}>
        {formatTime(message.timestamp)}
      </div>
    </div>
  );
};