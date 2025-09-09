import integrationService from './integrationService';

class SpecificationService {
  constructor() {
    this.baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:3001';
  }

  async generateSpecification(chatHistory, requirements) {
    try {
      const response = await fetch(`${this.baseUrl}/api/specifications/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          chatHistory,
          requirements,
          timestamp: Date.now()
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Failed to generate specification:', error);
      throw error;
    }
  }

  subscribeToProgress(jobId, onProgress, onComplete, onError) {
    const progressUnsubscribe = integrationService.subscribe('spec_progress', (data) => {
      if (data.jobId === jobId) {
        onProgress(data);
      }
    });

    const completeUnsubscribe = integrationService.subscribe('spec_complete', (data) => {
      if (data.jobId === jobId) {
        onComplete(data);
        cleanup();
      }
    });

    const errorUnsubscribe = integrationService.subscribe('spec_error', (data) => {
      if (data.jobId === jobId) {
        onError(data);
        cleanup();
      }
    });

    const cleanup = () => {
      progressUnsubscribe();
      completeUnsubscribe();
      errorUnsubscribe();
    };

    return cleanup;
  }
}

export default new SpecificationService();