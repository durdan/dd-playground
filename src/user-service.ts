export interface User {
  id: number;
  name: string;
  email: string;
}

export interface UserRepository {
  findById(id: number): Promise<User | null>;
  save(user: Omit<User, 'id'>): Promise<User>;
}

export class UserService {
  constructor(private userRepository: UserRepository) {}

  async getUserById(id: number): Promise<User> {
    if (!Number.isInteger(id) || id <= 0) {
      throw new Error('Invalid user ID: must be a positive integer');
    }

    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new Error(`User with ID ${id} not found`);
    }

    return user;
  }

  async createUser(name: string, email: string): Promise<User> {
    if (!name || name.trim().length === 0) {
      throw new Error('Name is required');
    }

    if (!this.isValidEmail(email)) {
      throw new Error('Invalid email format');
    }

    return await this.userRepository.save({ name: name.trim(), email });
  }

  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}