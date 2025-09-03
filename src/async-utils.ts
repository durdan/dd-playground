export class AsyncUtils {
  static async delay(ms: number): Promise<void> {
    if (ms < 0) {
      throw new Error('Delay must be non-negative');
    }
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  static async fetchData(url: string): Promise<any> {
    if (!url) {
      throw new Error('URL is required');
    }
    
    // Simulate API call
    await this.delay(100);
    
    if (url.includes('error')) {
      throw new Error('Network error');
    }
    
    return { data: `Response from ${url}`, timestamp: Date.now() };
  }
}