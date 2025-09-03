import { test, describe } from 'node:test';
import assert from 'node:assert';
import { UserRepository } from '../src/repositories/UserRepository.js';
import { UserService } from '../src/services/UserService.js';

describe('UserService', () => {
  let userService;

  test('setup', () => {
    const userRepository = new UserRepository();
    userService = new UserService(userRepository);
  });

  test('getUser - success', () => {
    const user = userService.getUser('1');
    assert.strictEqual(user.id, 1);
    assert.strictEqual(user.name, 'John Doe');
  });

  test('getUser - user not found', () => {
    assert.throws(() => userService.getUser('999'), /User not found/);
  });

  test('getUser - invalid ID', () => {
    assert.throws(() => userService.getUser('invalid'), /Invalid user ID/);
  });

  test('updateUser - success', () => {
    const updated = userService.updateUser('1', { name: 'John Updated' });
    assert.strictEqual(updated.name, 'John Updated');
    assert.strictEqual(updated.email, 'john@example.com');
  });

  test('updateUser - invalid email', () => {
    assert.throws(() => userService.updateUser('1', { email: 'invalid-email' }), /Invalid email format/);
  });

  test('updateUser - user not found', () => {
    assert.throws(() => userService.updateUser('999', { name: 'Test' }), /User not found/);
  });

  test('deleteUser - success', () => {
    const deleted = userService.deleteUser('2');
    assert.strictEqual(deleted.name, 'Jane Smith');
    assert.throws(() => userService.getUser('2'), /User not found/);
  });

  test('deleteUser - user not found', () => {
    assert.throws(() => userService.deleteUser('999'), /User not found/);
  });
});