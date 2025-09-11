const User = require('../models/user');

class UserService {
  constructor() {
    this.users = new Map();
    this.nextId = 1;
  }

  async getAllUsers() {
    return Array.from(this.users.values());
  }

  async getUserById(id) {
    const user = this.users.get(parseInt(id));
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  }

  async createUser(userData) {
    const errors = User.validate(userData);
    if (errors.length > 0) {
      throw new Error(`Validation failed: ${errors.join(', ')}`);
    }

    const existingUser = Array.from(this.users.values())
      .find(user => user.email === userData.email);
    
    if (existingUser) {
      throw new Error('Email already exists');
    }

    const user = new User(this.nextId++, userData.name, userData.email);
    this.users.set(user.id, user);
    return user;
  }

  async updateUser(id, userData) {
    const user = await this.getUserById(id);
    
    const errors = User.validate(userData);
    if (errors.length > 0) {
      throw new Error(`Validation failed: ${errors.join(', ')}`);
    }

    user.name = userData.name;
    user.email = userData.email;
    this.users.set(user.id, user);
    return user;
  }

  async deleteUser(id) {
    const user = await this.getUserById(id);
    this.users.delete(user.id);
    return user;
  }
}

module.exports = UserService;