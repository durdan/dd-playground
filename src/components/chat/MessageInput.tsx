import React, { useState, KeyboardEvent } from 'react';
import './MessageInput.css';

interface MessageInputProps {
  onSendMessage: (content: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  disabled = false,
  placeholder = "Type your message...",
}) => {
  const [content, setContent] = useState('');

  const handleSend = (): void => {
    const trimmedContent = content.trim();
    if (trimmedContent && !disabled) {
      onSendMessage(trimmedContent);
      setContent('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>): void => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="message-input">
      <textarea
        className="message-input__field"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder={placeholder}
        disabled={disabled}
        rows={1}
      />
      <button
        className="message-input__send"
        onClick={handleSend}
        disabled={disabled || !content.trim()}
        type="button"
      >
        Send
      </button>
    </div>
  );
};