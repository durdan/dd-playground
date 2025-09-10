import { v4 as uuidv4 } from 'uuid';
import { ChatRepository } from '../repositories/chatRepository';
import { AIService } from './aiService';
import { Conversation, Message, CreateConversationRequest, SendMessageRequest } from '../models/chat';

export class ChatService {
  constructor(
    private chatRepository: ChatRepository,
    private aiService: AIService
  ) {}

  async createConversation(userId: string, request: CreateConversationRequest): Promise<Conversation> {
    if (!userId) {
      throw new Error('User ID is required');
    }

    const conversation: Conversation = {
      id: uuidv4(),
      userId,
      title: request.title || 'New Conversation',
      createdAt: new Date(),
      updatedAt: new Date()
    };

    return this.chatRepository.createConversation(conversation);
  }

  async getUserConversations(userId: string): Promise<Conversation[]> {
    if (!userId) {
      throw new Error('User ID is required');
    }

    return this.chatRepository.getConversationsByUserId(userId);
  }

  async getConversation(conversationId: string, userId: string): Promise<Conversation> {
    if (!conversationId || !userId) {
      throw new Error('Conversation ID and User ID are required');
    }

    const conversation = await this.chatRepository.getConversationById(conversationId);
    if (!conversation) {
      throw new Error('Conversation not found');
    }

    if (conversation.userId !== userId) {
      throw new Error('Access denied');
    }

    return conversation;
  }

  async sendMessage(conversationId: string, userId: string, request: SendMessageRequest): Promise<{ userMessage: Message; aiMessage: Message }> {
    if (!conversationId || !userId || !request.content?.trim()) {
      throw new Error('Conversation ID, User ID, and message content are required');
    }

    // Verify conversation exists and user has access
    const conversation = await this.getConversation(conversationId, userId);

    // Create user message
    const userMessage: Message = {
      id: uuidv4(),
      conversationId,
      content: request.content.trim(),
      role: 'user',
      timestamp: new Date(),
      metadata: request.metadata
    };

    await this.chatRepository.addMessage(userMessage);

    // Get conversation history for AI context
    const conversationHistory = conversation.messages?.map(m => m.content) || [];

    // Generate AI response
    const aiResponse = await this.aiService.generateResponse(userMessage.content, conversationHistory);

    const aiMessage: Message = {
      id: uuidv4(),
      conversationId,
      content: aiResponse.content,
      role: 'assistant',
      timestamp: new Date(),
      metadata: aiResponse.metadata
    };

    await this.chatRepository.addMessage(aiMessage);

    return { userMessage, aiMessage };
  }

  async deleteConversation(conversationId: string, userId: string): Promise<void> {
    if (!conversationId || !userId) {
      throw new Error('Conversation ID and User ID are required');
    }

    // Verify conversation exists and user has access
    await this.getConversation(conversationId, userId);

    const deleted = await this.chatRepository.deleteConversation(conversationId);
    if (!deleted) {
      throw new Error('Failed to delete conversation');
    }
  }
}