const { connectDatabase } = require('./config/database');
const User = require('./models/User');

// Initialize database connection
const initializeApp = async () => {
  await connectDatabase();
  console.log('Application initialized successfully');
};

module.exports = {
  initializeApp,
  User
};