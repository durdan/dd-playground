export interface User {
  id: number;
  name: string;
  email: string;
  age: number;
}

export class UserService {
  private users: User[] = [];

  addUser(user: Omit<User, 'id'>): User {
    if (!user.name || !user.email) {
      throw new Error('Name and email are required');
    }
    if (user.age < 0 || user.age > 150) {
      throw new Error('Age must be between 0 and 150');
    }
    if (!this.isValidEmail(user.email)) {
      throw new Error('Invalid email format');
    }

    const newUser: User = {
      id: this.users.length + 1,
      ...user
    };
    this.users.push(newUser);
    return newUser;
  }

  getUserById(id: number): User | undefined {
    return this.users.find(user => user.id === id);
  }

  getAllUsers(): User[] {
    return [...this.users];
  }

  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}