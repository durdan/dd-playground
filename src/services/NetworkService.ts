import { RetryManager } from '../errors/RetryManager';

export interface RequestConfig {
  timeout?: number;
  retries?: number;
  headers?: Record<string, string>;
}

export class NetworkService {
  private static defaultTimeout = 30000; // 30 seconds

  static async request<T>(
    url: string, 
    options: RequestInit & RequestConfig = {}
  ): Promise<T> {
    const { timeout = this.defaultTimeout, retries = 3, ...fetchOptions } = options;

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      return await RetryManager.withRetry(async () => {
        const response = await fetch(url, {
          ...fetchOptions,
          signal: controller.signal
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
      }, { maxAttempts: retries });
    } catch (error) {
      if (error.name === 'AbortError') {
        throw new Error('Request timeout');
      }
      throw error;
    } finally {
      clearTimeout(timeoutId);
    }
  }
}