import { UserService, User } from '../user';

describe('UserService', () => {
  let userService: UserService;

  beforeEach(() => {
    userService = new UserService();
  });

  describe('addUser', () => {
    it('should add a valid user', () => {
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        age: 30
      };

      const user = userService.addUser(userData);

      expect(user).toEqual({
        id: 1,
        ...userData
      });
    });

    it('should throw error for missing name', () => {
      const userData = {
        name: '',
        email: 'john@example.com',
        age: 30
      };

      expect(() => userService.addUser(userData)).toThrow('Name and email are required');
    });

    it('should throw error for invalid email', () => {
      const userData = {
        name: 'John Doe',
        email: 'invalid-email',
        age: 30
      };

      expect(() => userService.addUser(userData)).toThrow('Invalid email format');
    });

    it('should throw error for invalid age', () => {
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        age: -5
      };

      expect(() => userService.addUser(userData)).toThrow('Age must be between 0 and 150');
    });

    it('should assign incremental IDs', () => {
      const user1 = userService.addUser({
        name: 'John',
        email: 'john@example.com',
        age: 30
      });

      const user2 = userService.addUser({
        name: 'Jane',
        email: 'jane@example.com',
        age: 25
      });

      expect(user1.id).toBe(1);
      expect(user2.id).toBe(2);
    });
  });

  describe('getUserById', () => {
    it('should return user by ID', () => {
      const addedUser = userService.addUser({
        name: 'John Doe',
        email: 'john@example.com',
        age: 30
      });

      const foundUser = userService.getUserById(1);
      expect(foundUser).toEqual(addedUser);
    });

    it('should return undefined for non-existent ID', () => {
      const foundUser = userService.getUserById(999);
      expect(foundUser).toBeUndefined();
    });
  });

  describe('getAllUsers', () => {
    it('should return all users', () => {
      userService.addUser({
        name: 'John',
        email: 'john@example.com',
        age: 30
      });

      userService.addUser({
        name: 'Jane',
        email: 'jane@example.com',
        age: 25
      });

      const users = userService.getAllUsers();
      expect(users).toHaveLength(2);
      expect(users[0].name).toBe('John');
      expect(users[1].name).toBe('Jane');
    });

    it('should return empty array when no users', () => {
      const users = userService.getAllUsers();
      expect(users).toEqual([]);
    });
  });
});