const mongoose = require('mongoose');

const DATABASE_CONFIG = {
  uri: process.env.MONGODB_URI || 'mongodb://localhost:27017/myapp',
  options: {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  }
};

const connectDatabase = async () => {
  try {
    await mongoose.connect(DATABASE_CONFIG.uri, DATABASE_CONFIG.options);
    console.log('MongoDB connected successfully');
  } catch (error) {
    console.error('MongoDB connection error:', error.message);
    process.exit(1);
  }
};

// Connection event handlers
mongoose.connection.on('connected', () => {
  console.log('Mongoose connected to MongoDB');
});

mongoose.connection.on('error', (error) => {
  console.error('Mongoose connection error:', error);
});

mongoose.connection.on('disconnected', () => {
  console.log('Mongoose disconnected from MongoDB');
});

// Graceful shutdown
process.on('SIGINT', async () => {
  await mongoose.connection.close();
  console.log('MongoDB connection closed through app termination');
  process.exit(0);
});

module.exports = { connectDatabase, DATABASE_CONFIG };