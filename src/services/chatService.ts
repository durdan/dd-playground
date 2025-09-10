import { Message } from '../types/chat';

class ChatService {
  private baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:3001';

  async sendMessage(content: string): Promise<Message> {
    if (!content.trim()) {
      throw new Error('Message content cannot be empty');
    }

    const response = await fetch(`${this.baseUrl}/api/chat/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content }),
    });

    if (!response.ok) {
      throw new Error(`Failed to send message: ${response.statusText}`);
    }

    return response.json();
  }

  generateMessageId(): string {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

export const chatService = new ChatService();