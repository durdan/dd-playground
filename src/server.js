const express = require('express');
const { Pool } = require('pg');
const redis = require('redis');
const promClient = require('prom-client');

class StagingApp {
  constructor() {
    this.app = express();
    this.port = process.env.PORT || 8080;
    this.setupMetrics();
    this.setupDatabase();
    this.setupRedis();
    this.setupRoutes();
  }

  setupMetrics() {
    // Create a Registry to register the metrics
    this.register = new promClient.Registry();
    
    // Add default metrics
    promClient.collectDefaultMetrics({ register: this.register });
    
    // Custom metrics
    this.httpRequestDuration = new promClient.Histogram({
      name: 'http_request_duration_seconds',
      help: 'Duration of HTTP requests in seconds',
      labelNames: ['method', 'route', 'status_code'],
      registers: [this.register]
    });

    this.httpRequestsTotal = new promClient.Counter({
      name: 'http_requests_total',
      help: 'Total number of HTTP requests',
      labelNames: ['method', 'route', 'status_code'],
      registers: [this.register]
    });
  }

  setupDatabase() {
    this.db = new Pool({
      connectionString: process.env.DATABASE_URL,
      max: 10,
      idleTimeoutMillis: 30000,
    });
  }

  async setupRedis() {
    this.redisClient = redis.createClient({
      url: process.env.REDIS_URL
    });
    
    this.redisClient.on('error', (err) => {
      console.error('Redis Client Error', err);
    });
    
    await this.redisClient.connect();
  }

  setupRoutes() {
    this.app.use(express.json());
    this.app.use(this.metricsMiddleware.bind(this));

    this.app.get('/health', this.healthCheck.bind(this));
    this.app.get('/metrics', this.getMetrics.bind(this));
    this.app.get('/config', this.getConfig.bind(this));
    this.app.get('/api/status', this.getStatus.bind(this));
  }

  metricsMiddleware(req, res, next) {
    const start = Date.now();
    
    res.on('finish', () => {
      const duration = (Date.now() - start) / 1000;
      const route = req.route ? req.route.path : req.path;
      
      this.httpRequestDuration
        .labels(req.method, route, res.statusCode)
        .observe(duration);
      
      this.httpRequestsTotal
        .labels(req.method, route, res.statusCode)
        .inc();
    });
    
    next();
  }

  async healthCheck(req, res) {
    try {
      // Check database
      await this.db.query('SELECT 1');
      
      // Check Redis
      await this.redisClient.ping();
      
      res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV,
        uptime: process.uptime()
      });
    } catch (error) {
      res.status(503).json({
        status: 'unhealthy',
        error: error.message,
        timestamp: new Date().toISOString()
      });
    }
  }

  async getMetrics(req, res) {
    res.set('Content-Type', this.register.contentType);
    res.end(await this.register.metrics());
  }

  getConfig(req, res) {
    // Only expose non-sensitive config
    res.json({
      environment: process.env.NODE_ENV,
      logLevel: process.env.LOG_LEVEL,
      port: this.port,
      hasApiKey: !!process.env.API_KEY,
      hasDatabase: !!process.env.DATABASE_URL,
      hasRedis: !!process.env.REDIS_URL
    });
  }

  async getStatus(req, res) {
    try {
      const dbResult = await this.db.query('SELECT NOW() as db_time');
      const redisInfo = await this.redisClient.info();
      
      res.json({
        status: 'operational',
        services: {
          database: { connected: true, time: dbResult.rows[0].db_time },
          redis: { connected: true, info: 'connected' },
          api: { version: '1.0.0', environment: process.env.NODE_ENV }
        }
      });
    } catch (error) {
      res.status(500).json({
        status: 'degraded',
        error: error.message
      });
    }
  }

  async start() {
    try {
      await this.setupRedis();
      
      this.app.listen(this.port, () => {
        console.log(`Staging app running on port ${this.port}`);
        console.log(`Environment: ${process.env.NODE_ENV}`);
        console.log(`Log Level: ${process.env.LOG_LEVEL}`);
      });
    } catch (error) {
      console.error('Failed to start application:', error);
      process.exit(1);
    }
  }
}

const app = new StagingApp();
app.start();

module.exports = StagingApp;