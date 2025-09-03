class UserStore {
  constructor() {
    this.users = new Map();
  }

  save(user) {
    this.users.set(user.id, user);
    return user;
  }

  findById(id) {
    return this.users.get(id);
  }

  findByEmail(email) {
    return Array.from(this.users.values()).find(user => user.email === email);
  }

  clear() {
    this.users.clear();
  }
}

module.exports = UserStore;