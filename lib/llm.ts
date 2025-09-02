import 'server-only';
import OpenAI from 'openai';

// TypeScript types for message structure
export type MessageRole = 'system' | 'user' | 'assistant';

export interface ChatMessage {
  role: MessageRole;
  content: string;
}

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

/**
 * Complete a chat conversation using OpenAI's GPT model
 * @param messages Array of chat messages
 * @returns Promise resolving to the assistant's response
 */
export async function chatComplete(messages: ChatMessage[]): Promise<string> {
  // Validate input
  if (!messages || messages.length === 0) {
    throw new Error('Messages array cannot be empty');
  }

  // Validate API key
  if (!process.env.OPENAI_API_KEY) {
    throw new Error('OPENAI_API_KEY environment variable is required');
  }

  // Validate message structure
  for (const message of messages) {
    if (!message.role || !message.content) {
      throw new Error('Each message must have role and content properties');
    }
    if (!['system', 'user', 'assistant'].includes(message.role)) {
      throw new Error(`Invalid message role: ${message.role}`);
    }
  }

  try {
    const completion = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: messages,
      temperature: 0.2,
    });

    const response = completion.choices[0]?.message?.content;
    
    if (!response) {
      throw new Error('No response received from OpenAI');
    }

    return response;
  } catch (error) {
    if (error instanceof OpenAI.APIError) {
      throw new Error(`OpenAI API error: ${error.message}`);
    }
    throw error;
  }
}