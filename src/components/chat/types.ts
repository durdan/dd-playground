export interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  specType?: string;
}

export interface SpecType {
  id: string;
  label: string;
  description: string;
}

export interface ChatState {
  messages: ChatMessage[];
  isTyping: boolean;
  selectedSpecType: string;
}