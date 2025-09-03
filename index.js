const { connectDB } = require('./config/database');
const User = require('./models/User');

// Example usage
const initializeApp = async () => {
  try {
    // Connect to database
    await connectDB();
    
    // Example: Create a user
    const newUser = new User({
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password123'
    });
    
    console.log('Database setup complete. Ready to use User model.');
    return { User };
  } catch (error) {
    console.error('App initialization failed:', error.message);
    process.exit(1);
  }
};

module.exports = { initializeApp, User };