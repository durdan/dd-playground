import React, { useState, useRef, KeyboardEvent } from 'react';
import { AttachmentHandler } from './AttachmentHandler';

interface MessageInputProps {
  onSendMessage: (content: string, attachments?: File[]) => void;
  disabled?: boolean;
  placeholder?: string;
  maxLength?: number;
}

export const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  disabled = false,
  placeholder = "Type your message...",
  maxLength = 2000
}) => {
  const [message, setMessage] = useState('');
  const [attachments, setAttachments] = useState<File[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = async () => {
    const trimmedMessage = message.trim();
    
    if (!trimmedMessage && attachments.length === 0) {
      return;
    }

    if (trimmedMessage.length > maxLength) {
      throw new Error(`Message too long. Maximum ${maxLength} characters allowed.`);
    }

    setIsSubmitting(true);
    
    try {
      await onSendMessage(trimmedMessage, attachments);
      setMessage('');
      setAttachments([]);
      
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    
    // Auto-resize textarea
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
  };

  const removeAttachment = (index: number) => {
    setAttachments(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="message-input-container">
      {attachments.length > 0 && (
        <div className="attachments-preview">
          {attachments.map((file, index) => (
            <div key={index} className="attachment-item">
              <span className="attachment-name">{file.name}</span>
              <button
                onClick={() => removeAttachment(index)}
                className="remove-attachment"
                type="button"
              >
                ×
              </button>
            </div>
          ))}
        </div>
      )}
      
      <div className="input-row">
        <AttachmentHandler
          onAttachmentsChange={setAttachments}
          maxFiles={5}
          maxFileSize={10 * 1024 * 1024} // 10MB
        />
        
        <textarea
          ref={textareaRef}
          value={message}
          onChange={handleTextareaChange}
          onKeyPress={handleKeyPress}
          placeholder={placeholder}
          disabled={disabled || isSubmitting}
          className="message-textarea"
          rows={1}
          maxLength={maxLength}
        />
        
        <button
          onClick={handleSubmit}
          disabled={disabled || isSubmitting || (!message.trim() && attachments.length === 0)}
          className="send-button"
          type="button"
        >
          {isSubmitting ? '⏳' : '📤'}
        </button>
      </div>
      
      <div className="input-footer">
        <span className="character-count">
          {message.length}/{maxLength}
        </span>
        <span className="input-hint">
          Press Enter to send, Shift+Enter for new line
        </span>
      </div>
    </div>
  );
};