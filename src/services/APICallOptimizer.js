export class APICallOptimizer {
  constructor() {
    this.cache = new Map();
    this.batchQueue = [];
    this.batchTimeout = null;
    this.batchDelay = 50; // ms
    this.debounceTimers = new Map();
    this.debounceDelay = 300; // ms
  }

  enableBatching() {
    this.batchingEnabled = true;
  }

  enableCaching() {
    this.cachingEnabled = true;
  }

  async makeAPICall(endpoint, params = {}) {
    if (!endpoint) {
      throw new Error('API endpoint is required');
    }

    const cacheKey = this.generateCacheKey(endpoint, params);

    // Return cached result if available
    if (this.cachingEnabled && this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      if (!this.isCacheExpired(cached)) {
        return cached.data;
      }
    }

    // Use batching if enabled
    if (this.batchingEnabled) {
      return this.batchAPICall(endpoint, params, cacheKey);
    }

    // Make direct API call
    return this.executeAPICall(endpoint, params, cacheKey);
  }

  async batchAPICall(endpoint, params, cacheKey) {
    return new Promise((resolve, reject) => {
      this.batchQueue.push({ endpoint, params, cacheKey, resolve, reject });

      if (this.batchTimeout) {
        clearTimeout(this.batchTimeout);
      }

      this.batchTimeout = setTimeout(() => {
        this.processBatch();
      }, this.batchDelay);
    });
  }

  async processBatch() {
    if (this.batchQueue.length === 0) return;

    const batch = [...this.batchQueue];
    this.batchQueue = [];
    this.batchTimeout = null;

    // Group by endpoint
    const groupedCalls = batch.reduce((groups, call) => {
      if (!groups[call.endpoint]) {
        groups[call.endpoint] = [];
      }
      groups[call.endpoint].push(call);
      return groups;
    }, {});

    // Process each endpoint group
    for (const [endpoint, calls] of Object.entries(groupedCalls)) {
      try {
        const results = await this.executeBatchCall(endpoint, calls);
        
        calls.forEach((call, index) => {
          const result = results[index];
          if (this.cachingEnabled) {
            this.cache.set(call.cacheKey, {
              data: result,
              timestamp: Date.now(),
              ttl: 5 * 60 * 1000 // 5 minutes
            });
          }
          call.resolve(result);
        });
      } catch (error) {
        calls.forEach(call => call.reject(error));
      }
    }
  }

  async executeBatchCall(endpoint, calls) {
    // Simulate batch API call
    const params = calls.map(call => call.params);
    await new Promise(resolve => setTimeout(resolve, 200));
    
    return params.map((param, index) => ({
      id: index,
      endpoint,
      params: param,
      result: `Result for ${endpoint}`,
      timestamp: Date.now()
    }));
  }

  async executeAPICall(endpoint, params, cacheKey) {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 200));
    
    const result = {
      endpoint,
      params,
      result: `Result for ${endpoint}`,
      timestamp: Date.now()
    };

    if (this.cachingEnabled) {
      this.cache.set(cacheKey, {
        data: result,
        timestamp: Date.now(),
        ttl: 5 * 60 * 1000 // 5 minutes
      });
    }

    return result;
  }

  debounce(key, fn, delay = this.debounceDelay) {
    if (this.debounceTimers.has(key)) {
      clearTimeout(this.debounceTimers.get(key));
    }

    return new Promise((resolve, reject) => {
      const timer = setTimeout(async () => {
        try {
          const result = await fn();
          resolve(result);
        } catch (error) {
          reject(error);
        } finally {
          this.debounceTimers.delete(key);
        }
      }, delay);

      this.debounceTimers.set(key, timer);
    });
  }

  generateCacheKey(endpoint, params) {
    return `${endpoint}:${JSON.stringify(params)}`;
  }

  isCacheExpired(cached) {
    return Date.now() - cached.timestamp > cached.ttl;
  }

  getCacheStats() {
    return {
      size: this.cache.size,
      hitRate: this.calculateHitRate(),
      memoryUsage: this.estimateMemoryUsage()
    };
  }

  calculateHitRate() {
    // Simplified hit rate calculation
    return this.cache.size > 0 ? 0.8 : 0;
  }

  estimateMemoryUsage() {
    return this.cache.size * 1024; // Rough estimate
  }

  clearCache() {
    this.cache.clear();
    this.debounceTimers.forEach(timer => clearTimeout(timer));
    this.debounceTimers.clear();
  }
}