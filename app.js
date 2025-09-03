const express = require('express');
const prometheus = require('prom-client');

const app = express();
const port = process.env.PORT || 3000;

// Prometheus metrics
const collectDefaultMetrics = prometheus.collectDefaultMetrics;
collectDefaultMetrics();

const httpRequestDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code']
});

const httpRequestsTotal = new prometheus.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code']
});

// Middleware for metrics
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const route = req.route ? req.route.path : req.path;
    
    httpRequestDuration
      .labels(req.method, route, res.statusCode)
      .observe(duration);
    
    httpRequestsTotal
      .labels(req.method, route, res.statusCode)
      .inc();
  });
  
  next();
});

app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    environment: process.env.NODE_ENV,
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Metrics endpoint for Prometheus
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', prometheus.register.contentType);
  res.end(await prometheus.register.metrics());
});

// Environment info endpoint (staging only)
app.get('/env-info', (req, res) => {
  if (process.env.NODE_ENV !== 'staging') {
    return res.status(404).json({ error: 'Not found' });
  }
  
  res.json({
    environment: process.env.NODE_ENV,
    logLevel: process.env.LOG_LEVEL,
    databaseConnected: !!process.env.DATABASE_URL,
    redisConnected: !!process.env.REDIS_URL
  });
});

// Sample API endpoint
app.get('/api/status', (req, res) => {
  res.json({
    message: 'API is running',
    environment: process.env.NODE_ENV,
    version: '1.0.0'
  });
});

app.listen(port, () => {
  console.log(`Server running on port ${port} in ${process.env.NODE_ENV} mode`);
});

module.exports = app;