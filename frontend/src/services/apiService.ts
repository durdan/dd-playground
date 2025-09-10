export interface ChatMessage {
  id: string;
  content: string;
  timestamp: Date;
  type: 'user' | 'assistant' | 'spec';
  specData?: GeneratedSpec;
}

export interface SpecGenerationRequest {
  message: string;
  context?: string[];
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = 'http://localhost:3001/api') {
    this.baseUrl = baseUrl;
  }

  async generateSpecification(request: SpecGenerationRequest): Promise<{ requestId: string }> {
    const response = await fetch(`${this.baseUrl}/generate-spec`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }

    return response.json();
  }

  async getChatHistory(): Promise<ChatMessage[]> {
    const response = await fetch(`${this.baseUrl}/chat-history`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch chat history: ${response.statusText}`);
    }

    return response.json();
  }
}

export const apiService = new ApiService();