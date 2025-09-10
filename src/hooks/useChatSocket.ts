import { useEffect, useRef, useState } from 'react';
import { Message } from '../types/chat';

interface UseChatSocketReturn {
  isConnected: boolean;
  sendMessage: (message: Message) => void;
  messages: Message[];
  isTyping: boolean;
}

export const useChatSocket = (onMessageReceived: (message: Message) => void): UseChatSocketReturn => {
  const [isConnected, setIsConnected] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    const wsUrl = process.env.REACT_APP_WS_URL || 'ws://localhost:3001/ws';
    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      setIsConnected(true);
    };

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.type === 'message') {
          const message: Message = {
            id: data.id,
            content: data.content,
            sender: data.sender,
            timestamp: new Date(data.timestamp),
            status: 'sent'
          };
          onMessageReceived(message);
        } else if (data.type === 'typing') {
          setIsTyping(data.isTyping);
        }
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    ws.current.onclose = () => {
      setIsConnected(false);
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };

    return () => {
      ws.current?.close();
    };
  }, [onMessageReceived]);

  const sendMessage = (message: Message) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({
        type: 'message',
        ...message
      }));
    }
  };

  return { isConnected, sendMessage, messages, isTyping };
};