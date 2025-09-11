import { Request, Response, NextFunction } from 'express';
import { validationErrorResponse } from '../utils/responseFormatter';

export const validateCreateConversation = (req: Request, res: Response, next: NextFunction) => {
  const { title } = req.body;
  const errors: string[] = [];

  if (!title || typeof title !== 'string') {
    errors.push('Title is required and must be a string');
  }

  if (title && title.trim().length === 0) {
    errors.push('Title cannot be empty');
  }

  if (title && title.length > 200) {
    errors.push('Title must be less than 200 characters');
  }

  if (errors.length > 0) {
    return res.status(400).json(validationErrorResponse(errors));
  }

  next();
};

export const validateSendMessage = (req: Request, res: Response, next: NextFunction) => {
  const { content, role } = req.body;
  const errors: string[] = [];

  if (!content || typeof content !== 'string') {
    errors.push('Content is required and must be a string');
  }

  if (content && content.trim().length === 0) {
    errors.push('Content cannot be empty');
  }

  if (!role || !['user', 'assistant'].includes(role)) {
    errors.push('Role must be either "user" or "assistant"');
  }

  if (errors.length > 0) {
    return res.status(400).json(validationErrorResponse(errors));
  }

  next();
};

export const validateSpecGeneration = (req: Request, res: Response, next: NextFunction) => {
  const { conversationId, specType } = req.body;
  const errors: string[] = [];

  if (!conversationId || typeof conversationId !== 'string') {
    errors.push('ConversationId is required and must be a string');
  }

  if (!specType || !['openapi', 'asyncapi', 'graphql'].includes(specType)) {
    errors.push('SpecType must be one of: openapi, asyncapi, graphql');
  }

  if (errors.length > 0) {
    return res.status(400).json(validationErrorResponse(errors));
  }

  next();
};