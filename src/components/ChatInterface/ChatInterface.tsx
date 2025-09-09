import React from 'react';
import { useChatState } from '../../hooks/useChatState';
import { MessageList } from '../MessageList/MessageList';
import { MessageInput } from '../MessageInput/MessageInput';
import styles from './ChatInterface.module.css';

interface ChatInterfaceProps {
  onSendMessage?: (message: string) => Promise<string>;
  title?: string;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  onSendMessage,
  title = "Chat"
}) => {
  const { messages, isLoading, addMessage, setLoading, clearMessages } = useChatState();

  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;

    // Add user message
    addMessage(message, 'user');

    if (onSendMessage) {
      setLoading(true);
      try {
        const response = await onSendMessage(message);
        addMessage(response, 'assistant');
      } catch (error) {
        addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
        console.error('Chat error:', error);
      } finally {
        setLoading(false);
      }
    } else {
      // Demo mode - echo message
      setTimeout(() => {
        addMessage(`Echo: ${message}`, 'assistant');
      }, 1000);
    }
  };

  return (
    <div className={styles.chatInterface}>
      <div className={styles.header}>
        <h2 className={styles.title}>{title}</h2>
        <button
          onClick={clearMessages}
          className={styles.clearButton}
          aria-label="Clear chat"
        >
          Clear
        </button>
      </div>
      
      <MessageList messages={messages} isLoading={isLoading} />
      
      <MessageInput
        onSendMessage={handleSendMessage}
        disabled={isLoading}
        placeholder="Type your message..."
      />
    </div>
  );
};