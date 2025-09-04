const express = require('express');
const { Pool } = require('pg');
const redis = require('redis');
const promClient = require('prom-client');

class EnvironmentConfig {
  constructor() {
    this.port = process.env.WEB_PORT || 3000;
    this.nodeEnv = process.env.NODE_ENV || 'development';
    this.databaseUrl = process.env.DATABASE_URL;
    this.redisUrl = process.env.REDIS_URL;
    this.apiKey = process.env.API_KEY;
    this.logLevel = process.env.LOG_LEVEL || 'info';
    
    this.validate();
  }

  validate() {
    const required = ['DATABASE_URL', 'REDIS_URL', 'API_KEY'];
    const missing = required.filter(key => !process.env[key]);
    
    if (missing.length > 0) {
      throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
    }
  }
}

class MetricsService {
  constructor() {
    this.register = new promClient.Registry();
    
    // Default metrics
    promClient.collectDefaultMetrics({ register: this.register });
    
    // Custom metrics
    this.httpRequestDuration = new promClient.Histogram({
      name: 'http_request_duration_seconds',
      help: 'Duration of HTTP requests in seconds',
      labelNames: ['method', 'route', 'status_code'],
      buckets: [0.1, 0.5, 1, 2, 5]
    });
    
    this.httpRequestTotal = new promClient.Counter({
      name: 'http_requests_total',
      help: 'Total number of HTTP requests',
      labelNames: ['method', 'route', 'status_code']
    });

    this.register.registerMetric(this.httpRequestDuration);
    this.register.registerMetric(this.httpRequestTotal);
  }

  recordRequest(method, route, statusCode, duration) {
    this.httpRequestTotal.inc({ method, route, status_code: statusCode });
    this.httpRequestDuration.observe({ method, route, status_code: statusCode }, duration);
  }

  getMetrics() {
    return this.register.metrics();
  }
}

class HealthService {
  constructor(dbPool, redisClient) {
    this.dbPool = dbPool;
    this.redisClient = redisClient;
  }

  async checkDatabase() {
    try {
      await this.dbPool.query('SELECT 1');
      return { status: 'healthy', message: 'Database connection OK' };
    } catch (error) {
      return { status: 'unhealthy', message: `Database error: ${error.message}` };
    }
  }

  async checkRedis() {
    try {
      await this.redisClient.ping();
      return { status: 'healthy', message: 'Redis connection OK' };
    } catch (error) {
      return { status: 'unhealthy', message: `Redis error: ${error.message}` };
    }
  }

  async getHealthStatus() {
    const [dbHealth, redisHealth] = await Promise.all([
      this.checkDatabase(),
      this.checkRedis()
    ]);

    const isHealthy = dbHealth.status === 'healthy' && redisHealth.status === 'healthy';

    return {
      status: isHealthy ? 'healthy' : 'unhealthy',
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV,
      services: {
        database: dbHealth,
        redis: redisHealth
      }
    };
  }
}

class Application {
  constructor() {
    this.config = new EnvironmentConfig();
    this.app = express();
    this.metricsService = new MetricsService();
    
    this.setupDatabase();
    this.setupRedis();
    this.setupMiddleware();
    this.setupRoutes();
  }

  setupDatabase() {
    this.dbPool = new Pool({
      connectionString: this.config.databaseUrl,
      max: 10,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });
  }

  setupRedis() {
    this.redisClient = redis.createClient({
      url: this.config.redisUrl
    });
    
    this.redisClient.on('error', (err) => {
      console.error('Redis Client Error', err);
    });
    
    this.redisClient.connect();
  }

  setupMiddleware() {
    this.app.use(express.json());
    
    // Metrics middleware
    this.app.use((req, res, next) => {
      const start = Date.now();
      
      res.on('finish', () => {
        const duration = (Date.now() - start) / 1000;
        this.metricsService.recordRequest(
          req.method,
          req.route?.path || req.path,
          res.statusCode,
          duration
        );
      });
      
      next();
    });
  }

  setupRoutes() {
    this.healthService = new HealthService(this.dbPool, this.redisClient);

    this.app.get('/health', async (req, res) => {
      try {
        const health = await this.healthService.getHealthStatus();
        const statusCode = health.status === 'healthy' ? 200 : 503;
        res.status(statusCode).json(health);
      } catch (error) {
        res.status(500).json({
          status: 'error',
          message: error.message,
          timestamp: new Date().toISOString()
        });
      }
    });

    this.app.get('/metrics', async (req, res) => {
      res.set('Content-Type', promClient.register.contentType);
      res.end(await this.metricsService.getMetrics());
    });

    this.app.get('/config', (req, res) => {
      res.json({
        environment: this.config.nodeEnv,
        port: this.config.port,
        logLevel: this.config.logLevel,
        timestamp: new Date().toISOString()
      });
    });

    this.app.get('/', (req, res) => {
      res.json({
        message: 'Staging Environment API',
        environment: this.config.nodeEnv,
        timestamp: new Date().toISOString()
      });
    });
  }

  async start() {
    try {
      this.app.listen(this.config.port, () => {
        console.log(`Server running on port ${this.config.port} in ${this.config.nodeEnv} mode`);
      });
    } catch (error) {
      console.error('Failed to start server:', error);
      process.exit(1);
    }
  }
}

// Start application
const app = new Application();
app.start();