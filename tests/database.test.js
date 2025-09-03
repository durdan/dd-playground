const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');
const { connectDatabase } = require('../config/database');
const User = require('../models/User');

let mongoServer;

beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  process.env.MONGODB_URI = mongoServer.getUri();
});

afterAll(async () => {
  await mongoose.connection.close();
  await mongoServer.stop();
});

beforeEach(async () => {
  await User.deleteMany({});
});

describe('Database Connection', () => {
  test('should connect to MongoDB successfully', async () => {
    await connectDatabase();
    expect(mongoose.connection.readyState).toBe(1); // 1 = connected
  });
});

describe('User Model', () => {
  test('should create a valid user', async () => {
    const userData = {
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password123'
    };

    const user = new User(userData);
    const savedUser = await user.save();

    expect(savedUser._id).toBeDefined();
    expect(savedUser.name).toBe(userData.name);
    expect(savedUser.email).toBe(userData.email);
    expect(savedUser.createdAt).toBeDefined();
    expect(savedUser.updatedAt).toBeDefined();
  });

  test('should fail validation for missing required fields', async () => {
    const user = new User({});

    await expect(user.save()).rejects.toThrow();
  });

  test('should fail validation for invalid email', async () => {
    const userData = {
      name: 'John Doe',
      email: 'invalid-email',
      password: 'password123'
    };

    const user = new User(userData);
    await expect(user.save()).rejects.toThrow();
  });

  test('should fail validation for short password', async () => {
    const userData = {
      name: 'John Doe',
      email: 'john@example.com',
      password: '123'
    };

    const user = new User(userData);
    await expect(user.save()).rejects.toThrow();
  });

  test('should enforce unique email constraint', async () => {
    const userData = {
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password123'
    };

    await new User(userData).save();
    const duplicateUser = new User(userData);
    
    await expect(duplicateUser.save()).rejects.toThrow();
  });

  test('should update updatedAt field on save', async () => {
    const user = new User({
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password123'
    });

    const savedUser = await user.save();
    const originalUpdatedAt = savedUser.updatedAt;

    // Wait a bit and update
    await new Promise(resolve => setTimeout(resolve, 10));
    savedUser.name = 'Jane Doe';
    const updatedUser = await savedUser.save();

    expect(updatedUser.updatedAt.getTime()).toBeGreaterThan(originalUpdatedAt.getTime());
  });
});