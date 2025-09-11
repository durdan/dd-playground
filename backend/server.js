const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const helmet = require('helmet');
require('dotenv').config();

const diagramRoutes = require('./routes/diagrams');
const { initDatabase } = require('./database/init');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: process.env.FRONTEND_URL || "http://localhost:3000",
    methods: ["GET", "POST"]
  }
});

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/diagrams', diagramRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Socket.io for real-time collaboration
io.on('connection', (socket) => {
  console.log('User connected:', socket.id);

  socket.on('join-diagram', (diagramId) => {
    socket.join(diagramId);
    console.log(`User ${socket.id} joined diagram ${diagramId}`);
  });

  socket.on('shape-added', (data) => {
    socket.to(data.diagramId).emit('shape-added', data.shape);
  });

  socket.on('shapes-updated', (data) => {
    socket.to(data.diagramId).emit('shapes-updated', data.shapes);
  });

  socket.on('disconnect', () => {
    console.log('User disconnected:', socket.id);
  });
});

// Initialize database and start server
const PORT = process.env.PORT || 3001;

initDatabase().then(() => {
  server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}).catch(error => {
  console.error('Failed to initialize database:', error);
  process.exit(1);
});