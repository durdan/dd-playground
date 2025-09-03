const bcrypt = require('bcrypt');
const Joi = require('joi');

class User {
  constructor(data) {
    this.id = data.id;
    this.email = data.email;
    this.name = data.name;
    this.password = data.password;
    this.createdAt = data.createdAt || new Date();
  }

  static validate(userData) {
    const schema = Joi.object({
      email: Joi.string().email().required(),
      name: Joi.string().min(2).max(50).required(),
      password: Joi.string().min(6).required()
    });

    return schema.validate(userData);
  }

  static validateUpdate(userData) {
    const schema = Joi.object({
      email: Joi.string().email(),
      name: Joi.string().min(2).max(50),
      password: Joi.string().min(6)
    }).min(1);

    return schema.validate(userData);
  }

  async hashPassword() {
    if (this.password) {
      this.password = await bcrypt.hash(this.password, 10);
    }
  }

  async comparePassword(plainPassword) {
    return bcrypt.compare(plainPassword, this.password);
  }

  toJSON() {
    const { password, ...userWithoutPassword } = this;
    return userWithoutPassword;
  }
}

module.exports = User;