import { UserService, UserRepository, User } from '../src/user-service';

describe('UserService', () => {
  let userService: UserService;
  let mockUserRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockUserRepository = {
      findById: jest.fn(),
      save: jest.fn()
    };
    userService = new UserService(mockUserRepository);
  });

  describe('getUserById', () => {
    it('should return user when found', async () => {
      const mockUser: User = { id: 1, name: 'John Doe', email: 'john@example.com' };
      mockUserRepository.findById.mockResolvedValue(mockUser);

      const result = await userService.getUserById(1);

      expect(result).toEqual(mockUser);
      expect(mockUserRepository.findById).toHaveBeenCalledWith(1);
    });

    it('should throw error when user not found', async () => {
      mockUserRepository.findById.mockResolvedValue(null);

      await expect(userService.getUserById(1)).rejects.toThrow('User with ID 1 not found');
    });

    it('should throw error for invalid ID', async () => {
      await expect(userService.getUserById(0)).rejects.toThrow('User ID must be a positive integer');
      await expect(userService.getUserById(-1)).rejects.toThrow('User ID must be a positive integer');
      await expect(userService.getUserById(1.5)).rejects.toThrow('User ID must be a positive integer');
    });
  });

  describe('createUser', () => {
    it('should create user with valid data', async () => {
      const newUser = { name: 'Jane Doe', email: 'jane@example.com' };
      const savedUser: User = { id: 1, ...newUser };
      mockUserRepository.save.mockResolvedValue(savedUser);

      const result = await userService.createUser(newUser.name, newUser.email);

      expect(result).toEqual(savedUser);
      expect(mockUserRepository.save).toHaveBeenCalledWith(newUser);
    });

    it('should trim whitespace from name', async () => {
      const savedUser: User = { id: 1, name: 'John Doe', email: 'john@example.com' };
      mockUserRepository.save.mockResolvedValue(savedUser);

      await userService.createUser('  John Doe  ', 'john@example.com');

      expect(mockUserRepository.save).toHaveBeenCalledWith({
        name: 'John Doe',
        email: 'john@example.com'
      });
    });

    it('should throw error for invalid name', async () => {
      await expect(userService.createUser('', 'john@example.com')).rejects.toThrow('Name is required');
      await expect(userService.createUser('   ', 'john@example.com')).rejects.toThrow('Name is required');
    });

    it('should throw error for invalid email', async () => {
      await expect(userService.createUser('John', '')).rejects.toThrow('Valid email is required');
      await expect(userService.createUser('John', 'invalid-email')).rejects.toThrow('Valid email is required');
      await expect(userService.createUser('John', 'john@')).rejects.toThrow('Valid email is required');
    });
  });
});