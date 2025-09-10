const { ChatService } = require('../../src/services/chat-service');
const { AIService } = require('../../src/services/ai-service');

jest.mock('../../src/services/ai-service');

describe('ChatService', () => {
  let chatService;
  let mockAIService;

  beforeEach(() => {
    mockAIService = {
      generateResponse: jest.fn(),
      analyzeForSpecification: jest.fn()
    };
    AIService.mockImplementation(() => mockAIService);
    chatService = new ChatService();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('addMessage', () => {
    it('should add user message to history', () => {
      const message = 'Hello, I need help with a project';
      
      chatService.addMessage('user', message);
      
      expect(chatService.getHistory()).toHaveLength(1);
      expect(chatService.getHistory()[0]).toEqual({
        role: 'user',
        content: message,
        timestamp: expect.any(Date)
      });
    });

    it('should add assistant message to history', () => {
      const message = 'How can I help you today?';
      
      chatService.addMessage('assistant', message);
      
      expect(chatService.getHistory()).toHaveLength(1);
      expect(chatService.getHistory()[0]).toEqual({
        role: 'assistant',
        content: message,
        timestamp: expect.any(Date)
      });
    });

    it('should reject invalid role', () => {
      expect(() => {
        chatService.addMessage('invalid', 'message');
      }).toThrow('Invalid role: invalid');
    });

    it('should reject empty message', () => {
      expect(() => {
        chatService.addMessage('user', '');
      }).toThrow('Message content cannot be empty');
    });

    it('should reject non-string message', () => {
      expect(() => {
        chatService.addMessage('user', null);
      }).toThrow('Message content must be a string');
    });
  });

  describe('processUserMessage', () => {
    it('should process user message and get AI response', async () => {
      const userMessage = 'I want to build a todo app';
      const aiResponse = 'I can help you build a todo app. What features do you need?';
      
      mockAIService.generateResponse.mockResolvedValue(aiResponse);

      const result = await chatService.processUserMessage(userMessage);

      expect(mockAIService.generateResponse).toHaveBeenCalledWith([
        { role: 'user', content: userMessage, timestamp: expect.any(Date) }
      ]);
      expect(result).toBe(aiResponse);
      expect(chatService.getHistory()).toHaveLength(2);
    });

    it('should handle AI service errors gracefully', async () => {
      const userMessage = 'Test message';
      const error = new Error('AI service unavailable');
      
      mockAIService.generateResponse.mockRejectedValue(error);

      await expect(chatService.processUserMessage(userMessage)).rejects.toThrow('AI service unavailable');
      expect(chatService.getHistory()).toHaveLength(1); // Only user message added
    });
  });

  describe('clearHistory', () => {
    it('should clear all messages from history', () => {
      chatService.addMessage('user', 'Message 1');
      chatService.addMessage('assistant', 'Response 1');
      
      expect(chatService.getHistory()).toHaveLength(2);
      
      chatService.clearHistory();
      
      expect(chatService.getHistory()).toHaveLength(0);
    });
  });

  describe('getLastUserMessage', () => {
    it('should return the last user message', () => {
      chatService.addMessage('user', 'First message');
      chatService.addMessage('assistant', 'Response');
      chatService.addMessage('user', 'Second message');

      const lastUserMessage = chatService.getLastUserMessage();
      
      expect(lastUserMessage.content).toBe('Second message');
      expect(lastUserMessage.role).toBe('user');
    });

    it('should return null when no user messages exist', () => {
      chatService.addMessage('assistant', 'Only assistant message');
      
      expect(chatService.getLastUserMessage()).toBeNull();
    });
  });
});