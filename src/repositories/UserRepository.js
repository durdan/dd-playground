import { User } from '../models/User.js';

export class UserRepository {
  constructor() {
    this.users = new Map();
    this.nextId = 1;
    
    // Seed with sample data
    this.create('John Doe', 'john@example.com');
    this.create('Jane Smith', 'jane@example.com');
  }

  create(name, email) {
    const user = new User(this.nextId++, name, email);
    this.users.set(user.id, user);
    return user;
  }

  findById(id) {
    return this.users.get(parseInt(id));
  }

  update(id, updates) {
    const user = this.findById(id);
    if (!user) return null;
    
    Object.assign(user, updates, { updatedAt: new Date().toISOString() });
    return user;
  }

  delete(id) {
    const user = this.findById(id);
    if (!user) return null;
    
    this.users.delete(parseInt(id));
    return user;
  }
}