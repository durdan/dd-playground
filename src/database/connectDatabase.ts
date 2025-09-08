import mongoose from 'mongoose';

const DATABASE_URL = process.env.DATABASE_URL || 'mongodb://localhost/dd-playground';

const connectDatabase = async () => {
  try {
    await mongoose.connect(DATABASE_URL, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log('Database connected successfully.');
  } catch (error) {
    console.error('Database connection failed:', error);
    process.exit(1);
  }
};

export default connectDatabase;