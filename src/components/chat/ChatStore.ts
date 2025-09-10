import { ChatMessage, ChatState } from './types';

class ChatStore {
  private state: ChatState = {
    messages: [],
    isLoading: false,
    error: null,
  };

  private listeners: Array<(state: ChatState) => void> = [];

  getState(): ChatState {
    return { ...this.state };
  }

  subscribe(listener: (state: ChatState) => void): () => void {
    this.listeners.push(listener);
    return () => {
      const index = this.listeners.indexOf(listener);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }

  private notify(): void {
    this.listeners.forEach(listener => listener(this.getState()));
  }

  addMessage(message: ChatMessage): void {
    this.state.messages.push(message);
    this.notify();
  }

  updateMessage(id: string, updates: Partial<ChatMessage>): void {
    const index = this.state.messages.findIndex(msg => msg.id === id);
    if (index > -1) {
      this.state.messages[index] = { ...this.state.messages[index], ...updates };
      this.notify();
    }
  }

  setLoading(isLoading: boolean): void {
    this.state.isLoading = isLoading;
    this.notify();
  }

  setError(error: string | null): void {
    this.state.error = error;
    this.notify();
  }

  clearMessages(): void {
    this.state.messages = [];
    this.notify();
  }
}

export const chatStore = new ChatStore();