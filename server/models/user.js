class User {
  constructor(id, name, email, createdAt = new Date()) {
    this.id = id;
    this.name = name;
    this.email = email;
    this.createdAt = createdAt;
  }

  static validate(userData) {
    const errors = [];
    
    if (!userData.name || userData.name.trim().length < 2) {
      errors.push('Name must be at least 2 characters long');
    }
    
    if (!userData.email || !this.isValidEmail(userData.email)) {
      errors.push('Valid email is required');
    }
    
    return errors;
  }

  static isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}

module.exports = User;