import express from 'express';

export function createUserRoutes(userService) {
  const router = express.Router();

  // GET /users/:id
  router.get('/:id', async (req, res) => {
    try {
      const user = userService.getUser(req.params.id);
      res.json(user);
    } catch (error) {
      const status = error.message === 'User not found' ? 404 : 400;
      res.status(status).json({ error: error.message });
    }
  });

  // PUT /users/:id
  router.put('/:id', async (req, res) => {
    try {
      const user = userService.updateUser(req.params.id, req.body);
      res.json(user);
    } catch (error) {
      const status = error.message === 'User not found' ? 404 : 400;
      res.status(status).json({ error: error.message });
    }
  });

  // DELETE /users/:id
  router.delete('/:id', async (req, res) => {
    try {
      const user = userService.deleteUser(req.params.id);
      res.json({ message: 'User deleted successfully', user });
    } catch (error) {
      const status = error.message === 'User not found' ? 404 : 400;
      res.status(status).json({ error: error.message });
    }
  });

  return router;
}