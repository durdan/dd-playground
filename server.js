const express = require('express');
const createRateLimitMiddleware = require('./src/middleware/rateLimitMiddleware');
const authRoutes = require('./src/routes/authRoutes');
const protectedRoutes = require('./src/routes/protectedRoutes');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Rate limiting - 50 requests per minute for auth routes
const authRateLimit = createRateLimitMiddleware(50, 60000);
// Rate limiting - 200 requests per minute for protected routes  
const apiRateLimit = createRateLimitMiddleware(200, 60000);

// Routes
app.use('/auth', authRateLimit, authRoutes);
app.use('/api', apiRateLimit, protectedRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}

module.exports = app;