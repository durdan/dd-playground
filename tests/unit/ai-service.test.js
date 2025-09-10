const { AIService } = require('../../src/services/ai-service');
const OpenAI = require('openai');

jest.mock('openai');

describe('AIService', () => {
  let aiService;
  let mockOpenAI;

  beforeEach(() => {
    mockOpenAI = {
      chat: {
        completions: {
          create: jest.fn()
        }
      }
    };
    OpenAI.mockImplementation(() => mockOpenAI);
    aiService = new AIService();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('generateResponse', () => {
    it('should generate response from chat history', async () => {
      const chatHistory = [
        { role: 'user', content: 'Hello', timestamp: new Date() }
      ];
      const mockResponse = {
        choices: [{
          message: { content: 'Hello! How can I help you?' }
        }]
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      const result = await aiService.generateResponse(chatHistory);

      expect(mockOpenAI.chat.completions.create).toHaveBeenCalledWith({
        model: 'gpt-3.5-turbo',
        messages: [
          {
            role: 'system',
            content: expect.stringContaining('You are a helpful assistant')
          },
          { role: 'user', content: 'Hello' }
        ],
        max_tokens: 1000,
        temperature: 0.7
      });
      expect(result).toBe('Hello! How can I help you?');
    });

    it('should handle empty chat history', async () => {
      await expect(aiService.generateResponse([])).rejects.toThrow('Chat history cannot be empty');
    });

    it('should handle OpenAI API errors', async () => {
      const chatHistory = [
        { role: 'user', content: 'Hello', timestamp: new Date() }
      ];
      const error = new Error('API rate limit exceeded');
      
      mockOpenAI.chat.completions.create.mockRejectedValue(error);

      await expect(aiService.generateResponse(chatHistory)).rejects.toThrow('API rate limit exceeded');
    });

    it('should handle missing response content', async () => {
      const chatHistory = [
        { role: 'user', content: 'Hello', timestamp: new Date() }
      ];
      const mockResponse = {
        choices: [{ message: {} }]
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      await expect(aiService.generateResponse(chatHistory)).rejects.toThrow('No response content received from AI');
    });
  });

  describe('analyzeForSpecification', () => {
    it('should analyze chat for specification generation', async () => {
      const chatHistory = [
        { role: 'user', content: 'I want to build a todo app with user authentication', timestamp: new Date() },
        { role: 'assistant', content: 'Great! What features do you need?', timestamp: new Date() },
        { role: 'user', content: 'CRUD operations, due dates, and categories', timestamp: new Date() }
      ];
      
      const mockAnalysis = {
        choices: [{
          message: {
            content: JSON.stringify({
              projectType: 'web application',
              features: ['user authentication', 'CRUD operations', 'due dates', 'categories'],
              requirements: ['secure login', 'data persistence', 'responsive design']
            })
          }
        }]
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockAnalysis);

      const result = await aiService.analyzeForSpecification(chatHistory);

      expect(mockOpenAI.chat.completions.create).toHaveBeenCalledWith({
        model: 'gpt-3.5-turbo',
        messages: expect.arrayContaining([
          expect.objectContaining({
            role: 'system',
            content: expect.stringContaining('analyze the conversation and extract')
          })
        ]),
        max_tokens: 1500,
        temperature: 0.3
      });
      
      expect(result).toEqual({
        projectType: 'web application',
        features: ['user authentication', 'CRUD operations', 'due dates', 'categories'],
        requirements: ['secure login', 'data persistence', 'responsive design']
      });
    });

    it('should handle invalid JSON response', async () => {
      const chatHistory = [
        { role: 'user', content: 'Build an app', timestamp: new Date() }
      ];
      
      const mockResponse = {
        choices: [{
          message: { content: 'Invalid JSON response' }
        }]
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      await expect(aiService.analyzeForSpecification(chatHistory)).rejects.toThrow('Failed to parse specification analysis');
    });
  });
});