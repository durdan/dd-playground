const express = require('express');
const { errorHandler, notFoundHandler } = require('./middleware/errorMiddleware');
const exampleRoutes = require('./routes/exampleRoutes');

const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/api', exampleRoutes);

// Handle unhandled routes (must be after all other routes)
app.use(notFoundHandler);

// Global error handler (must be last middleware)
app.use(errorHandler);

const PORT = process.env.PORT || 3000;

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}

module.exports = app;