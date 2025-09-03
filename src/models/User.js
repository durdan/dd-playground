export class User {
  constructor(id, name, email) {
    this.id = id;
    this.name = name;
    this.email = email;
    this.createdAt = new Date().toISOString();
    this.updatedAt = new Date().toISOString();
  }
}