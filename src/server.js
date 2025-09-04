const express = require('express');
const { Pool } = require('pg');
const client = require('prom-client');

class AppServer {
  constructor() {
    this.app = express();
    this.port = process.env.PORT || 3000;
    this.metricsPort = process.env.METRICS_PORT || 9090;
    this.setupDatabase();
    this.setupMetrics();
    this.setupRoutes();
  }

  setupDatabase() {
    this.db = new Pool({
      connectionString: process.env.DATABASE_URL,
      max: 10,
      idleTimeoutMillis: 30000,
    });
  }

  setupMetrics() {
    this.register = new client.Registry();
    client.collectDefaultMetrics({ register: this.register });
    
    this.httpRequestsTotal = new client.Counter({
      name: 'http_requests_total',
      help: 'Total number of HTTP requests',
      labelNames: ['method', 'route', 'status'],
      registers: [this.register]
    });

    this.httpRequestDuration = new client.Histogram({
      name: 'http_request_duration_seconds',
      help: 'Duration of HTTP requests in seconds',
      labelNames: ['method', 'route'],
      registers: [this.register]
    });
  }

  setupRoutes() {
    // Metrics middleware
    this.app.use((req, res, next) => {
      const start = Date.now();
      res.on('finish', () => {
        const duration = (Date.now() - start) / 1000;
        this.httpRequestsTotal.inc({
          method: req.method,
          route: req.route?.path || req.path,
          status: res.statusCode
        });
        this.httpRequestDuration.observe({
          method: req.method,
          route: req.route?.path || req.path
        }, duration);
      });
      next();
    });

    this.app.get('/health', async (req, res) => {
      try {
        await this.db.query('SELECT 1');
        res.json({
          status: 'healthy',
          environment: process.env.NODE_ENV,
          timestamp: new Date().toISOString(),
          database: 'connected'
        });
      } catch (error) {
        res.status(503).json({
          status: 'unhealthy',
          error: error.message
        });
      }
    });

    this.app.get('/metrics', (req, res) => {
      res.set('Content-Type', this.register.contentType);
      res.end(this.register.metrics());
    });

    this.app.get('/', (req, res) => {
      res.json({
        message: 'Staging Environment API',
        environment: process.env.NODE_ENV,
        version: '1.0.0'
      });
    });

    this.app.get('/config', (req, res) => {
      res.json({
        environment: process.env.NODE_ENV,
        logLevel: process.env.LOG_LEVEL,
        hasApiKey: !!process.env.API_KEY,
        databaseConnected: !!this.db
      });
    });
  }

  async start() {
    try {
      await this.db.query('SELECT NOW()');
      console.log('Database connected successfully');
      
      this.app.listen(this.port, () => {
        console.log(`Server running on port ${this.port}`);
        console.log(`Environment: ${process.env.NODE_ENV}`);
        console.log(`Metrics available on port ${this.metricsPort}`);
      });
    } catch (error) {
      console.error('Failed to start server:', error);
      process.exit(1);
    }
  }
}

const server = new AppServer();
server.start();