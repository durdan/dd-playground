import { LazySpecificationLoader } from './LazySpecificationLoader.js';
import { APICallOptimizer } from './APICallOptimizer.js';
import { RealtimeManager } from './RealtimeManager.js';
import { PerformanceMonitor } from './PerformanceMonitor.js';

export class PerformanceOptimizer {
  constructor() {
    this.specLoader = new LazySpecificationLoader();
    this.apiOptimizer = new APICallOptimizer();
    this.realtimeManager = new RealtimeManager();
    this.monitor = new PerformanceMonitor();
    this.isOptimized = false;
  }

  async optimizeChatInterface() {
    if (this.isOptimized) return;

    try {
      // Start performance monitoring
      this.monitor.startMonitoring();

      // Initialize lazy loading
      await this.specLoader.initialize();

      // Setup API call optimization
      this.apiOptimizer.enableBatching();
      this.apiOptimizer.enableCaching();

      // Initialize real-time connections
      await this.realtimeManager.connect();

      this.isOptimized = true;
      console.log('Chat interface optimization complete');
    } catch (error) {
      console.error('Optimization failed:', error);
      throw new Error(`Failed to optimize chat interface: ${error.message}`);
    }
  }

  async analyzePerformance() {
    const metrics = this.monitor.getMetrics();
    const bottlenecks = this.identifyBottlenecks(metrics);
    
    return {
      metrics,
      bottlenecks,
      recommendations: this.generateRecommendations(bottlenecks)
    };
  }

  identifyBottlenecks(metrics) {
    const bottlenecks = [];
    
    if (metrics.apiResponseTime > 1000) {
      bottlenecks.push('slow_api_calls');
    }
    if (metrics.renderTime > 16) {
      bottlenecks.push('slow_rendering');
    }
    if (metrics.memoryUsage > 100 * 1024 * 1024) {
      bottlenecks.push('high_memory_usage');
    }
    
    return bottlenecks;
  }

  generateRecommendations(bottlenecks) {
    const recommendations = [];
    
    bottlenecks.forEach(bottleneck => {
      switch (bottleneck) {
        case 'slow_api_calls':
          recommendations.push('Enable API call batching and caching');
          break;
        case 'slow_rendering':
          recommendations.push('Implement virtual scrolling for large lists');
          break;
        case 'high_memory_usage':
          recommendations.push('Implement lazy loading for specifications');
          break;
      }
    });
    
    return recommendations;
  }

  cleanup() {
    this.realtimeManager.disconnect();
    this.monitor.stopMonitoring();
    this.specLoader.clearCache();
    this.apiOptimizer.clearCache();
    this.isOptimized = false;
  }
}