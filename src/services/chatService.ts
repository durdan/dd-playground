import { v4 as uuidv4 } from 'uuid';
import { Message, Conversation, CreateConversationRequest, SendMessageRequest, SpecGenerationRequest } from '../models/chat';

// In-memory storage (replace with database in production)
const conversations: Map<string, Conversation> = new Map();
const messages: Map<string, Message[]> = new Map();

export class ChatService {
  static createConversation(request: CreateConversationRequest): Conversation {
    const conversation: Conversation = {
      id: uuidv4(),
      title: request.title.trim(),
      createdAt: new Date(),
      updatedAt: new Date(),
      messageCount: 0
    };

    conversations.set(conversation.id, conversation);
    messages.set(conversation.id, []);

    return conversation;
  }

  static getConversations(): Conversation[] {
    return Array.from(conversations.values()).sort(
      (a, b) => b.updatedAt.getTime() - a.updatedAt.getTime()
    );
  }

  static getConversation(id: string): Conversation | null {
    return conversations.get(id) || null;
  }

  static getMessages(conversationId: string): Message[] {
    if (!conversations.has(conversationId)) {
      throw new Error('Conversation not found');
    }

    return messages.get(conversationId) || [];
  }

  static sendMessage(conversationId: string, request: SendMessageRequest): Message {
    const conversation = conversations.get(conversationId);
    if (!conversation) {
      throw new Error('Conversation not found');
    }

    const message: Message = {
      id: uuidv4(),
      conversationId,
      content: request.content.trim(),
      role: request.role,
      timestamp: new Date(),
      metadata: request.metadata
    };

    const conversationMessages = messages.get(conversationId) || [];
    conversationMessages.push(message);
    messages.set(conversationId, conversationMessages);

    // Update conversation
    conversation.messageCount = conversationMessages.length;
    conversation.updatedAt = new Date();
    conversations.set(conversationId, conversation);

    return message;
  }

  static async generateSpec(request: SpecGenerationRequest): Promise<any> {
    const conversation = conversations.get(request.conversationId);
    if (!conversation) {
      throw new Error('Conversation not found');
    }

    const conversationMessages = messages.get(request.conversationId) || [];
    if (conversationMessages.length === 0) {
      throw new Error('No messages found in conversation');
    }

    // Mock spec generation based on conversation content
    const content = conversationMessages.map(m => m.content).join('\n');
    
    switch (request.specType) {
      case 'openapi':
        return this.generateOpenAPISpec(content, request.options);
      case 'asyncapi':
        return this.generateAsyncAPISpec(content, request.options);
      case 'graphql':
        return this.generateGraphQLSpec(content, request.options);
      default:
        throw new Error('Unsupported spec type');
    }
  }

  private static generateOpenAPISpec(content: string, options?: Record<string, any>): any {
    return {
      openapi: '3.0.0',
      info: {
        title: 'Generated API',
        version: '1.0.0',
        description: `Generated from chat conversation`
      },
      paths: {
        '/example': {
          get: {
            summary: 'Example endpoint',
            description: `Generated from: ${content.substring(0, 100)}...`,
            responses: {
              '200': {
                description: 'Success',
                content: {
                  'application/json': {
                    schema: {
                      type: 'object',
                      properties: {
                        message: { type: 'string' }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    };
  }

  private static generateAsyncAPISpec(content: string, options?: Record<string, any>): any {
    return {
      asyncapi: '2.6.0',
      info: {
        title: 'Generated Async API',
        version: '1.0.0',
        description: `Generated from chat conversation`
      },
      channels: {
        'example/channel': {
          description: `Generated from: ${content.substring(0, 100)}...`,
          publish: {
            message: {
              payload: {
                type: 'object',
                properties: {
                  data: { type: 'string' }
                }
              }
            }
          }
        }
      }
    };
  }

  private static generateGraphQLSpec(content: string, options?: Record<string, any>): any {
    return {
      schema: `
        type Query {
          example: String
        }
        
        type Mutation {
          createExample(input: String!): String
        }
        
        # Generated from: ${content.substring(0, 100)}...
      `
    };
  }
}