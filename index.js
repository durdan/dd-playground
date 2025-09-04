require('dotenv').config();
const { connectDB } = require('./config/database');
const User = require('./models/User');

const main = async () => {
  // Connect to database
  await connectDB();

  // Example usage
  try {
    const newUser = new User({
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password123'
    });

    const savedUser = await newUser.save();
    console.log('User created:', savedUser);
  } catch (error) {
    console.error('Error creating user:', error.message);
  }
};

// Only run if this file is executed directly
if (require.main === module) {
  main();
}

module.exports = { connectDB, User };