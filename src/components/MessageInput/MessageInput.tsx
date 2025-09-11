import React, { useState, useRef, useEffect } from 'react';
import { SpecType } from '../../types/chat';
import { SpecTypeSelector } from '../SpecTypeSelector/SpecTypeSelector';
import styles from './MessageInput.module.css';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  currentSpecType: SpecType;
  onSpecTypeChange: (specType: SpecType) => void;
  disabled?: boolean;
  placeholder?: string;
}

export const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  currentSpecType,
  onSpecTypeChange,
  disabled = false,
  placeholder = "Type your message..."
}) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!message.trim() || disabled) return;
    
    try {
      onSendMessage(message);
      setMessage('');
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  return (
    <div className={styles.container}>
      <div className={styles.controls}>
        <SpecTypeSelector
          currentSpecType={currentSpecType}
          onSpecTypeChange={onSpecTypeChange}
          disabled={disabled}
        />
      </div>
      
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.inputContainer}>
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={disabled}
            className={styles.textarea}
            rows={1}
          />
          <button
            type="submit"
            disabled={!message.trim() || disabled}
            className={styles.sendButton}
            aria-label="Send message"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
          </button>
        </div>
      </form>
    </div>
  );
};