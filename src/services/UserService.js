export class UserService {
  constructor(userRepository) {
    this.userRepository = userRepository;
  }

  getUser(id) {
    this.validateId(id);
    const user = this.userRepository.findById(id);
    
    if (!user) {
      throw new Error('User not found');
    }
    
    return user;
  }

  updateUser(id, updates) {
    this.validateId(id);
    this.validateUpdateData(updates);
    
    const user = this.userRepository.update(id, updates);
    if (!user) {
      throw new Error('User not found');
    }
    
    return user;
  }

  deleteUser(id) {
    this.validateId(id);
    const user = this.userRepository.delete(id);
    
    if (!user) {
      throw new Error('User not found');
    }
    
    return user;
  }

  validateId(id) {
    const numId = parseInt(id);
    if (isNaN(numId) || numId <= 0) {
      throw new Error('Invalid user ID');
    }
  }

  validateUpdateData(data) {
    if (!data || typeof data !== 'object') {
      throw new Error('Update data is required');
    }

    if (data.name !== undefined && (!data.name || typeof data.name !== 'string')) {
      throw new Error('Name must be a non-empty string');
    }

    if (data.email !== undefined) {
      if (!data.email || typeof data.email !== 'string') {
        throw new Error('Email must be a non-empty string');
      }
      if (!this.isValidEmail(data.email)) {
        throw new Error('Invalid email format');
      }
    }
  }

  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}