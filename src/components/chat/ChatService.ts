import { ChatMessage, ChatService } from './types';

class DefaultChatService implements ChatService {
  private apiBase: string;

  constructor(apiBase: string = '/api/chat') {
    this.apiBase = apiBase;
  }

  async sendMessage(content: string): Promise<ChatMessage> {
    if (!content.trim()) {
      throw new Error('Message content cannot be empty');
    }

    const response = await fetch(`${this.apiBase}/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content: content.trim() }),
    });

    if (!response.ok) {
      throw new Error(`Failed to send message: ${response.statusText}`);
    }

    const data = await response.json();
    return {
      id: data.id || Date.now().toString(),
      content: data.content || content,
      timestamp: new Date(data.timestamp || Date.now()),
      sender: data.sender || 'assistant',
    };
  }

  async getMessages(): Promise<ChatMessage[]> {
    const response = await fetch(`${this.apiBase}/messages`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch messages: ${response.statusText}`);
    }

    const data = await response.json();
    return data.map((msg: any) => ({
      id: msg.id,
      content: msg.content,
      timestamp: new Date(msg.timestamp),
      sender: msg.sender,
    }));
  }
}

export const chatService = new DefaultChatService();