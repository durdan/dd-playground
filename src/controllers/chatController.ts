import { Request, Response, NextFunction } from 'express';
import { ChatService } from '../services/chatService';

export class ChatController {
  constructor(private chatService: ChatService) {}

  createConversation = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const userId = req.user?.id; // Assuming auth middleware sets req.user
      if (!userId) {
        return res.status(401).json({ error: 'Authentication required' });
      }

      const conversation = await this.chatService.createConversation(userId, req.body);
      res.status(201).json(conversation);
    } catch (error) {
      next(error);
    }
  };

  getConversations = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const userId = req.user?.id;
      if (!userId) {
        return res.status(401).json({ error: 'Authentication required' });
      }

      const conversations = await this.chatService.getUserConversations(userId);
      res.json(conversations);
    } catch (error) {
      next(error);
    }
  };

  getConversation = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const userId = req.user?.id;
      if (!userId) {
        return res.status(401).json({ error: 'Authentication required' });
      }

      const conversation = await this.chatService.getConversation(req.params.id, userId);
      res.json(conversation);
    } catch (error) {
      next(error);
    }
  };

  sendMessage = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const userId = req.user?.id;
      if (!userId) {
        return res.status(401).json({ error: 'Authentication required' });
      }

      const result = await this.chatService.sendMessage(req.params.id, userId, req.body);
      res.json(result);
    } catch (error) {
      next(error);
    }
  };

  deleteConversation = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const userId = req.user?.id;
      if (!userId) {
        return res.status(401).json({ error: 'Authentication required' });
      }

      await this.chatService.deleteConversation(req.params.id, userId);
      res.status(204).send();
    } catch (error) {
      next(error);
    }
  };
}