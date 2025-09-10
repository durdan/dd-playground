import { Message, Conversation } from '../models/chat';

// In-memory storage for demo - replace with actual database
const conversations = new Map<string, Conversation>();
const messages = new Map<string, Message[]>();

export class ChatRepository {
  async createConversation(conversation: Conversation): Promise<Conversation> {
    conversations.set(conversation.id, conversation);
    messages.set(conversation.id, []);
    return conversation;
  }

  async getConversationsByUserId(userId: string): Promise<Conversation[]> {
    return Array.from(conversations.values())
      .filter(conv => conv.userId === userId)
      .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime());
  }

  async getConversationById(id: string): Promise<Conversation | null> {
    const conversation = conversations.get(id);
    if (!conversation) return null;

    const conversationMessages = messages.get(id) || [];
    return {
      ...conversation,
      messages: conversationMessages
    };
  }

  async addMessage(message: Message): Promise<Message> {
    const conversationMessages = messages.get(message.conversationId) || [];
    conversationMessages.push(message);
    messages.set(message.conversationId, conversationMessages);

    // Update conversation timestamp
    const conversation = conversations.get(message.conversationId);
    if (conversation) {
      conversation.updatedAt = new Date();
      conversations.set(message.conversationId, conversation);
    }

    return message;
  }

  async deleteConversation(id: string): Promise<boolean> {
    const deleted = conversations.delete(id);
    messages.delete(id);
    return deleted;
  }

  async conversationExists(id: string): Promise<boolean> {
    return conversations.has(id);
  }
}