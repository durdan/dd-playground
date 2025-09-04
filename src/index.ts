import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { healthRouter } from './routes/health';
import { errorHandler } from './middleware/errorHandler';
import { config } from './config';

const app = express();

// Security middleware
app.use(helmet());
app.use(cors());

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/health', healthRouter);

// Error handling middleware (must be last)
app.use(errorHandler);

const server = app.listen(config.port, () => {
  console.log(`Server running on port ${config.port}`);
});

export { app, server };