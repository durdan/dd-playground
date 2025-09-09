// This file is specifically for server-side operations related to Large Language Models (LLMs).
import { Configuration, OpenAIApi } from "openai";

// Define the message role types
type MessageRole = "system" | "user" | "assistant";

// Define the message structure
interface Message {
  role: MessageRole;
  content: string;
}

// Setup OpenAI client
const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

// Function to generate chat responses based on input messages
export async function chatComplete(messages: Message[]): Promise<string> {
  try {
    const response = await openai.createChatCompletion({
      model: "gpt-4o-mini",
      messages: messages.map(message => ({
        role: message.role,
        content: message.content
      })),
      temperature: 0.2
    });
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error("Failed to generate chat response:", error);
    throw new Error("Failed to generate chat response");
  }
}
