import { Request, Response, NextFunction } from 'express';
import { body, param, validationResult } from 'express-validator';

export const validateRequest = (req: Request, res: Response, next: NextFunction) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      error: 'Validation failed',
      details: errors.array()
    });
  }
  next();
};

export const validateCreateConversation = [
  body('title').optional().isString().trim().isLength({ min: 1, max: 100 }),
  validateRequest
];

export const validateSendMessage = [
  param('id').isUUID(),
  body('content').isString().trim().isLength({ min: 1, max: 5000 }),
  body('metadata').optional().isObject(),
  validateRequest
];

export const validateConversationId = [
  param('id').isUUID(),
  validateRequest
];