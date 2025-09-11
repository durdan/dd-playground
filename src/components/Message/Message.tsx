import React from 'react';
import { Message as MessageType } from '../../types/chat';
import styles from './Message.module.css';

interface MessageProps {
  message: MessageType;
}

export const Message: React.FC<MessageProps> = ({ message }) => {
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`${styles.message} ${styles[message.sender]}`}>
      <div className={styles.content}>
        {message.content}
      </div>
      <div className={styles.metadata}>
        <span className={styles.time}>{formatTime(message.timestamp)}</span>
        {message.specType && (
          <span className={styles.specType}>{message.specType}</span>
        )}
      </div>
    </div>
  );
};