import { Router } from 'express';
import { ChatController } from '../controllers/chatController';
import { ChatService } from '../services/chatService';
import { ChatRepository } from '../repositories/chatRepository';
import { AIService } from '../services/aiService';
import {
  validateCreateConversation,
  validateSendMessage,
  validateConversationId
} from '../middleware/validation';

// Initialize dependencies
const chatRepository = new ChatRepository();
const aiService = new AIService();
const chatService = new ChatService(chatRepository, aiService);
const chatController = new ChatController(chatService);

const router = Router();

// Create new conversation
router.post('/conversations', validateCreateConversation, chatController.createConversation);

// Get user's conversations
router.get('/conversations', chatController.getConversations);

// Get specific conversation with messages
router.get('/conversations/:id', validateConversationId, chatController.getConversation);

// Send message to conversation
router.post('/conversations/:id/messages', validateSendMessage, chatController.sendMessage);

// Delete conversation
router.delete('/conversations/:id', validateConversationId, chatController.deleteConversation);

export default router;