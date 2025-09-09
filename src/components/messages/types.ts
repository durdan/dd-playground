export interface BaseMessage {
  id: string;
  timestamp: Date;
  content: string;
}

export interface UserMessage extends BaseMessage {
  type: 'user';
  avatar?: string;
}

export interface SystemMessage extends BaseMessage {
  type: 'system';
  variant?: 'info' | 'success' | 'warning' | 'error';
}

export interface SpecPreview extends BaseMessage {
  type: 'spec';
  language: string;
  filename?: string;
  isCollapsible?: boolean;
}

export interface LoadingMessage {
  id: string;
  type: 'loading';
  message?: string;
}

export type Message = UserMessage | SystemMessage | SpecPreview | LoadingMessage;