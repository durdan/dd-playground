const express = require('express');
const http = require('http');
const cors = require('cors');
const integrationService = require('./services/integrationService');
const specificationRoutes = require('./routes/specifications');

const app = express();
const server = http.createServer(app);

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/specifications', specificationRoutes);

// Initialize WebSocket integration
integrationService.initialize(server);

// Error handling
app.use((error, req, res, next) => {
  console.error('Unhandled error:', error);
  res.status(500).json({ error: 'Internal server error' });
});

const PORT = process.env.PORT || 3001;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;