import { Router, Request, Response } from 'express';
import { ChatService } from '../services/chatService';
import { successResponse, errorResponse } from '../utils/responseFormatter';
import { 
  validateCreateConversation, 
  validateSendMessage, 
  validateSpecGeneration 
} from '../middleware/validation';

const router = Router();

// Create conversation
router.post('/conversations', validateCreateConversation, (req: Request, res: Response) => {
  try {
    const conversation = ChatService.createConversation(req.body);
    res.status(201).json(successResponse(conversation, 'Conversation created successfully'));
  } catch (error) {
    res.status(500).json(errorResponse('Failed to create conversation'));
  }
});

// Get all conversations
router.get('/conversations', (req: Request, res: Response) => {
  try {
    const conversations = ChatService.getConversations();
    res.json(successResponse(conversations));
  } catch (error) {
    res.status(500).json(errorResponse('Failed to fetch conversations'));
  }
});

// Get messages for a conversation
router.get('/conversations/:id/messages', (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const messages = ChatService.getMessages(id);
    res.json(successResponse(messages));
  } catch (error) {
    if (error instanceof Error && error.message === 'Conversation not found') {
      res.status(404).json(errorResponse('Conversation not found'));
    } else {
      res.status(500).json(errorResponse('Failed to fetch messages'));
    }
  }
});

// Send message to conversation
router.post('/conversations/:id/messages', validateSendMessage, (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const message = ChatService.sendMessage(id, req.body);
    res.status(201).json(successResponse(message, 'Message sent successfully'));
  } catch (error) {
    if (error instanceof Error && error.message === 'Conversation not found') {
      res.status(404).json(errorResponse('Conversation not found'));
    } else {
      res.status(500).json(errorResponse('Failed to send message'));
    }
  }
});

// Generate specification from conversation
router.post('/spec-generation', validateSpecGeneration, async (req: Request, res: Response) => {
  try {
    const spec = await ChatService.generateSpec(req.body);
    res.json(successResponse(spec, 'Specification generated successfully'));
  } catch (error) {
    if (error instanceof Error) {
      if (error.message === 'Conversation not found') {
        res.status(404).json(errorResponse('Conversation not found'));
      } else if (error.message === 'No messages found in conversation') {
        res.status(400).json(errorResponse('No messages found in conversation'));
      } else if (error.message === 'Unsupported spec type') {
        res.status(400).json(errorResponse('Unsupported spec type'));
      } else {
        res.status(500).json(errorResponse('Failed to generate specification'));
      }
    } else {
      res.status(500).json(errorResponse('Failed to generate specification'));
    }
  }
});

export default router;