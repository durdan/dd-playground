const { connectDatabase } = require('./config/database');
const User = require('./models/User');

// Initialize database connection
const initializeApp = async () => {
  await connectDatabase();
  
  // Example usage
  console.log('Application initialized with MongoDB connection');
  console.log('User model ready for use');
};

// Export for use in other modules
module.exports = {
  connectDatabase,
  User,
  initializeApp
};

// Run if this file is executed directly
if (require.main === module) {
  initializeApp().catch(console.error);
}