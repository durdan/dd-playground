export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  specType?: SpecType;
}

export type SpecType = 'general' | 'technical' | 'creative' | 'analytical';

export interface ChatState {
  messages: Message[];
  currentSpecType: SpecType;
  isLoading: boolean;
}