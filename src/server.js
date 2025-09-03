const express = require('express');
const { Pool } = require('pg');
const redis = require('redis');
const promClient = require('prom-client');

class AppServer {
  constructor() {
    this.app = express();
    this.port = process.env.PORT || 3000;
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
      buckets: [0.1, 0.5, 1, 2, 5]
    });
    
    this.register.registerMetric(this.httpRequestDuration);
  }

  setupDatabase() {
    if (!process.env.DATABASE_URL) {
      throw new Error('DATABASE_URL environment variable is required');
    }
    
    this.db = new Pool({
      connectionString: process.env.DATABASE_URL,
    });
  }

  setupRedis() {
    if (!process.env.REDIS_URL) {
      throw new Error('REDIS_URL environment variable is required');
    }
    
    this.redisClient = redis.createClient({
      url: process.env.REDIS_URL
    });
    
    this.redisClient.on('error', (err) => {
      console.error('Redis Client Error', err);
    });
  }

  setupRoutes() {
    this.app.use(express.json());
    
    // Metrics middleware
    this.app.use((req, res, next) => {
      const start = Date.now();
      
      res.on('finish', () => {
        const duration = (Date.now() - start) / 1000;
        this.httpRequestDuration
          .labels(req.method, req.route?.path || req.path, res.statusCode)
          .observe(duration);
      });
      
      next();
    });

    // Health check endpoint
    this.app.get('/health', async (req, res) => {
      try {
        // Check database
        await this.db.query('SELECT 1');
        
        // Check Redis
        await this.redisClient.ping();
        
        res.json({
          status: 'healthy',
          environment: process.env.NODE_ENV,
          timestamp: new Date().toISOString(),
          services: {
            database: 'connected',
            redis: 'connected'
          }
        });
      } catch (error) {
        res.status(503).json({
          status: 'unhealthy',
          error: error.message,
          timestamp: new Date().toISOString()
        });
      }
    });

    // Metrics endpoint
    this.app.get('/metrics', async (req, res) => {
      res.set('Content-Type', this.register.contentType);
      res.end(await this.register.metrics());
    });

    // API endpoints
    this.app.get('/api/config', (req, res) => {
      res.json({
        environment: process.env.NODE_ENV,
        logLevel: process.env.LOG_LEVEL,
        hasApiKey: !!process.env.API_KEY
      });
    });

    this.app.get('/api/status', async (req, res) => {
      try {
        const dbResult = await this.db.query('SELECT NOW() as current_time');
        const redisInfo = await this.redisClient.info();
        
        res.json({
          database: {
            connected: true,
            currentTime: dbResult.rows[0].current_time
          },
          redis: {
            connected: true,
            info: redisInfo.split('\r\n')[1] // Server info line
          }
        });
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });
  }

  async start() {
    try {
      await this.redisClient.connect();
      console.log('Connected to Redis');
      
      this.app.listen(this.port, () => {
        console.log(`Server running on port ${this.port} in ${process.env.NODE_ENV} mode`);
      });
    } catch (error) {
      console.error('Failed to start server:', error);
      process.exit(1);
    }
  }
}

// Start server if this file is run directly
if (require.main === module) {
  const server = new AppServer();
  server.start();
}

module.exports = AppServer;