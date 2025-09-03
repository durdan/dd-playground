import express from 'express';
import { UserRepository } from './repositories/UserRepository.js';
import { UserService } from './services/UserService.js';
import { createUserRoutes } from './routes/userRoutes.js';

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Dependencies
const userRepository = new UserRepository();
const userService = new UserService(userRepository);

// Routes
app.use('/users', createUserRoutes(userService));

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'OK' });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

export { app, userService };