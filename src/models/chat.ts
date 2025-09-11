export interface Message {
  id: string;
  conversationId: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  metadata?: Record<string, any>;
}

export interface Conversation {
  id: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
  messageCount: number;
}

export interface CreateConversationRequest {
  title: string;
}

export interface SendMessageRequest {
  content: string;
  role: 'user' | 'assistant';
  metadata?: Record<string, any>;
}

export interface SpecGenerationRequest {
  conversationId: string;
  specType: 'openapi' | 'asyncapi' | 'graphql';
  options?: Record<string, any>;
}