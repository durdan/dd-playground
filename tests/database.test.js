const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');
const { connectDB } = require('../config/database');
const User = require('../models/User');

let mongoServer;

beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  process.env.MONGODB_URI = mongoServer.getUri();
});

afterAll(async () => {
  await mongoose.connection.dropDatabase();
  await mongoose.connection.close();
  await mongoServer.stop();
});

beforeEach(async () => {
  await User.deleteMany({});
});

describe('Database Connection', () => {
  test('should connect to MongoDB', async () => {
    const connection = await connectDB();
    expect(connection.connection.readyState).toBe(1);
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
  });

  test('should fail with invalid email', async () => {
    const userData = {
      name: 'John Doe',
      email: 'invalid-email',
      password: 'password123'
    };

    const user = new User(userData);
    
    await expect(user.save()).rejects.toThrow();
  });

  test('should fail with missing required fields', async () => {
    const user = new User({});
    
    await expect(user.save()).rejects.toThrow();
  });

  test('should fail with short password', async () => {
    const userData = {
      name: 'John Doe',
      email: 'john@example.com',
      password: '123'
    };

    const user = new User(userData);
    
    await expect(user.save()).rejects.toThrow();
  });

  test('should not return password in JSON', async () => {
    const userData = {
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password123'
    };

    const user = new User(userData);
    const savedUser = await user.save();
    const userJSON = savedUser.toJSON();

    expect(userJSON.password).toBeUndefined();
    expect(userJSON.name).toBe(userData.name);
  });

  test('should enforce unique email constraint', async () => {
    const userData = {
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password123'
    };

    const user1 = new User(userData);
    await user1.save();

    const user2 = new User(userData);
    
    await expect(user2.save()).rejects.toThrow();
  });
});