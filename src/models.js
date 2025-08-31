class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
    this.id = Date.now();
  }

  validate() {
    return this.name && this.email && this.email.includes('@');
  }
}

class Product {
  constructor(name, price) {
    this.name = name;
    this.price = price;
    this.id = Date.now();
  }
}

module.exports = { User, Product };