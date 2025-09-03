class RateLimiter {
  constructor(maxRequests = 100, windowMs = 60000) { // 100 requests per minute
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
    this.clients = new Map();
  }

  isAllowed(clientId) {
    const now = Date.now();
    const client = this.clients.get(clientId);

    if (!client) {
      this.clients.set(clientId, {
        requests: 1,
        resetTime: now + this.windowMs
      });
      return { allowed: true, remaining: this.maxRequests - 1 };
    }

    if (now > client.resetTime) {
      // Reset window
      client.requests = 1;
      client.resetTime = now + this.windowMs;
      return { allowed: true, remaining: this.maxRequests - 1 };
    }

    if (client.requests >= this.maxRequests) {
      return { 
        allowed: false, 
        remaining: 0,
        resetTime: client.resetTime 
      };
    }

    client.requests++;
    return { 
      allowed: true, 
      remaining: this.maxRequests - client.requests 
    };
  }

  cleanup() {
    const now = Date.now();
    for (const [clientId, client] of this.clients.entries()) {
      if (now > client.resetTime) {
        this.clients.delete(clientId);
      }
    }
  }
}

const createRateLimitMiddleware = (maxRequests = 100, windowMs = 60000) => {
  const limiter = new RateLimiter(maxRequests, windowMs);
  
  // Cleanup expired entries every 5 minutes
  setInterval(() => limiter.cleanup(), 5 * 60 * 1000);

  return (req, res, next) => {
    const clientId = req.ip || req.connection.remoteAddress || 'unknown';
    const result = limiter.isAllowed(clientId);

    res.set({
      'X-RateLimit-Limit': maxRequests,
      'X-RateLimit-Remaining': result.remaining,
      'X-RateLimit-Reset': result.resetTime ? new Date(result.resetTime).toISOString() : null
    });

    if (!result.allowed) {
      return res.status(429).json({
        error: 'Too many requests. Please try again later.',
        retryAfter: Math.ceil((result.resetTime - Date.now()) / 1000)
      });
    }

    next();
  };
};

module.exports = createRateLimitMiddleware;