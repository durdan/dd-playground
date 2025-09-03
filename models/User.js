class User {
  constructor(email, password, id = null) {
    this.id = id || Date.now().toString();
    this.email = email;
    this.password = password;
    this.createdAt = new Date();
  }

  static validate(email, password) {
    const errors = [];
    
    if (!email || !email.includes('@')) {
      errors.push('Valid email is required');
    }
    
    if (!password || password.length < 6) {
      errors.push('Password must be at least 6 characters');
    }
    
    return errors;
  }

  toJSON() {
    return {
      id: this.id,
      email: this.email,
      createdAt: this.createdAt
    };
  }
}

module.exports = User;