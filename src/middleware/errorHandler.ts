import { Request, Response, NextFunction } from 'express';

export const errorHandler = (error: Error, req: Request, res: Response, next: NextFunction) => {
  console.error('Error:', error.message);

  if (error.message === 'Conversation not found') {
    return res.status(404).json({ error: error.message });
  }

  if (error.message === 'Access denied') {
    return res.status(403).json({ error: error.message });
  }

  if (error.message.includes('required')) {
    return res.status(400).json({ error: error.message });
  }

  res.status(500).json({ error: 'Internal server error' });
};