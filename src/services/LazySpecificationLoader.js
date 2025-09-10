export class LazySpecificationLoader {
  constructor() {
    this.cache = new Map();
    this.loadingPromises = new Map();
    this.chunkSize = 50; // Load specifications in chunks
  }

  async initialize() {
    // Pre-load essential specifications
    await this.preloadEssentials();
  }

  async loadSpecification(id) {
    if (!id) {
      throw new Error('Specification ID is required');
    }

    // Return cached version if available
    if (this.cache.has(id)) {
      return this.cache.get(id);
    }

    // Return existing loading promise if in progress
    if (this.loadingPromises.has(id)) {
      return this.loadingPromises.get(id);
    }

    // Start loading
    const loadingPromise = this.fetchSpecification(id);
    this.loadingPromises.set(id, loadingPromise);

    try {
      const spec = await loadingPromise;
      this.cache.set(id, spec);
      return spec;
    } finally {
      this.loadingPromises.delete(id);
    }
  }

  async loadSpecificationChunk(ids) {
    if (!Array.isArray(ids) || ids.length === 0) {
      return [];
    }

    const chunks = this.chunkArray(ids, this.chunkSize);
    const results = [];

    for (const chunk of chunks) {
      const chunkPromises = chunk.map(id => this.loadSpecification(id));
      const chunkResults = await Promise.all(chunkPromises);
      results.push(...chunkResults);
    }

    return results;
  }

  async preloadEssentials() {
    // Load frequently used specifications
    const essentialIds = ['common', 'ui-components', 'api-endpoints'];
    await Promise.all(essentialIds.map(id => this.loadSpecification(id)));
  }

  async fetchSpecification(id) {
    // Simulate API call with delay
    await new Promise(resolve => setTimeout(resolve, 100));
    
    return {
      id,
      name: `Specification ${id}`,
      content: `Content for specification ${id}`,
      size: Math.floor(Math.random() * 1000) + 100,
      loadedAt: Date.now()
    };
  }

  chunkArray(array, size) {
    const chunks = [];
    for (let i = 0; i < array.length; i += size) {
      chunks.push(array.slice(i, i + size));
    }
    return chunks;
  }

  getCacheStats() {
    return {
      size: this.cache.size,
      loading: this.loadingPromises.size,
      memoryUsage: this.estimateMemoryUsage()
    };
  }

  estimateMemoryUsage() {
    let totalSize = 0;
    for (const spec of this.cache.values()) {
      totalSize += spec.size || 0;
    }
    return totalSize;
  }

  clearCache() {
    this.cache.clear();
    this.loadingPromises.clear();
  }
}