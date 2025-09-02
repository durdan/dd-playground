import { chatComplete, ChatMessage } from '../llm';

// Mock OpenAI
jest.mock('openai', () => {
  return jest.fn().mockImplementation(() => ({
    chat: {
      completions: {
        create: jest.fn(),
      },
    },
  }));
});

const mockOpenAI = require('openai');
const mockCreate = mockOpenAI().chat.completions.create;

describe('chatComplete', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    process.env.OPENAI_API_KEY = 'test-api-key';
  });

  afterEach(() => {
    delete process.env.OPENAI_API_KEY;
  });

  it('should return response from OpenAI', async () => {
    const mockResponse = {
      choices: [{ message: { content: 'Hello, how can I help you?' } }],
    };
    mockCreate.mockResolvedValue(mockResponse);

    const messages: ChatMessage[] = [
      { role: 'user', content: 'Hello' },
    ];

    const result = await chatComplete(messages);
    expect(result).toBe('Hello, how can I help you?');
    expect(mockCreate).toHaveBeenCalledWith({
      model: 'gpt-4o-mini',
      messages: messages,
      temperature: 0.2,
    });
  });

  it('should throw error for empty messages array', async () => {
    await expect(chatComplete([])).rejects.toThrow('Messages array cannot be empty');
  });

  it('should throw error when API key is missing', async () => {
    delete process.env.OPENAI_API_KEY;
    const messages: ChatMessage[] = [{ role: 'user', content: 'Hello' }];
    
    await expect(chatComplete(messages)).rejects.toThrow('OPENAI_API_KEY environment variable is required');
  });

  it('should throw error for invalid message role', async () => {
    const messages = [{ role: 'invalid' as any, content: 'Hello' }];
    
    await expect(chatComplete(messages)).rejects.toThrow('Invalid message role: invalid');
  });

  it('should throw error for missing message content', async () => {
    const messages = [{ role: 'user', content: '' }];
    
    await expect(chatComplete(messages)).rejects.toThrow('Each message must have role and content properties');
  });

  it('should handle OpenAI API errors', async () => {
    const apiError = new (mockOpenAI.APIError as any)('Rate limit exceeded');
    mockCreate.mockRejectedValue(apiError);

    const messages: ChatMessage[] = [{ role: 'user', content: 'Hello' }];
    
    await expect(chatComplete(messages)).rejects.toThrow('OpenAI API error: Rate limit exceeded');
  });

  it('should throw error when no response content', async () => {
    const mockResponse = {
      choices: [{ message: { content: null } }],
    };
    mockCreate.mockResolvedValue(mockResponse);

    const messages: ChatMessage[] = [{ role: 'user', content: 'Hello' }];
    
    await expect(chatComplete(messages)).rejects.toThrow('No response received from OpenAI');
  });
});