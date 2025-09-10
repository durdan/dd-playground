import { ConversationState, Message } from './types';

export const conversationSelectors = {
  getMessagesByRole: (state: ConversationState, role: Message['role']): Message[] =>
    state.messages.filter(message => message.role === role),

  getRecentMessages: (state: ConversationState, count: number): Message[] =>
    state.messages.slice(-count),

  getMessagesWithErrors: (state: ConversationState): Message[] =>
    state.messages.filter(message => message.metadata?.error),

  getCurrentSpecId: (state: ConversationState): string | null =>
    state.currentSpecProgress?.specId || null,

  getSpecProgress: (state: ConversationState): number =>
    state.currentSpecProgress?.progress || 0,

  isSpecGenerating: (state: ConversationState): boolean =>
    state.currentSpecProgress?.stage === 'generating' ||
    state.currentSpecProgress?.stage === 'analyzing' ||
    state.currentSpecProgress?.stage === 'reviewing',

  getMessageCount: (state: ConversationState): number =>
    state.messages.length,

  hasReachedMaxHistory: (state: ConversationState): boolean =>
    state.messages.length >= state.userPreferences.maxHistorySize,
};