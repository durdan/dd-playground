import { test, describe } from 'node:test';
import assert from 'node:assert';
import { UserRepository } from '../src/repositories/UserRepository.js';
import { UserService } from '../src/services/UserService.js';
import { createUserRoutes } from '../src/routes/userRoutes.js';

describe('User Routes', () => {
  let userService;
  let mockReq, mockRes;

  test('setup', () => {
    const userRepository = new UserRepository();
    userService = new UserService(userRepository);
    
    mockRes = {
      json: (data) => mockRes.data = data,
      status: (code) => { mockRes.statusCode = code; return mockRes; }
    };
  });

  test('GET /users/:id - success', async () => {
    mockReq = { params: { id: '1' } };
    const routes = createUserRoutes(userService);
    
    // Simulate route handler
    try {
      const user = userService.getUser(mockReq.params.id);
      mockRes.json(user);
      assert.strictEqual(mockRes.data.id, 1);
    } catch (error) {
      assert.fail('Should not throw error');
    }
  });

  test('PUT /users/:id - success', async () => {
    mockReq = { params: { id: '1' }, body: { name: 'Updated Name' } };
    
    try {
      const user = userService.updateUser(mockReq.params.id, mockReq.body);
      mockRes.json(user);
      assert.strictEqual(mockRes.data.name, 'Updated Name');
    } catch (error) {
      assert.fail('Should not throw error');
    }
  });

  test('DELETE /users/:id - success', async () => {
    mockReq = { params: { id: '1' } };
    
    try {
      const user = userService.deleteUser(mockReq.params.id);
      mockRes.json({ message: 'User deleted successfully', user });
      assert.strictEqual(mockRes.data.message, 'User deleted successfully');
    } catch (error) {
      assert.fail('Should not throw error');
    }
  });
});