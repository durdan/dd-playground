export interface WebSocketMessage {
  type: 'spec_generation_start' | 'spec_generation_progress' | 'spec_generation_complete' | 'error';
  data: any;
  requestId?: string;
}

export interface SpecGenerationProgress {
  stage: string;
  progress: number;
  message: string;
}

export interface GeneratedSpec {
  id: string;
  title: string;
  content: string;
  timestamp: Date;
}

class WebSocketService {
  private ws: WebSocket | null = null;
  private listeners: Map<string, (message: WebSocketMessage) => void> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  connect(url: string): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(url);
        
        this.ws.onopen = () => {
          console.log('WebSocket connected');
          this.reconnectAttempts = 0;
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data);
            this.notifyListeners(message);
          } catch (error) {
            console.error('Failed to parse WebSocket message:', error);
          }
        };

        this.ws.onclose = () => {
          console.log('WebSocket disconnected');
          this.attemptReconnect(url);
        };

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          reject(error);
        };
      } catch (error) {
        reject(error);
      }
    });
  }

  private attemptReconnect(url: string): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      setTimeout(() => {
        console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);
        this.connect(url);
      }, 2000 * this.reconnectAttempts);
    }
  }

  subscribe(eventType: string, callback: (message: WebSocketMessage) => void): () => void {
    this.listeners.set(eventType, callback);
    return () => this.listeners.delete(eventType);
  }

  private notifyListeners(message: WebSocketMessage): void {
    this.listeners.forEach((callback) => callback(message));
  }

  send(message: any): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      throw new Error('WebSocket is not connected');
    }
  }

  disconnect(): void {
    this.ws?.close();
    this.listeners.clear();
  }
}

export const websocketService = new WebSocketService();