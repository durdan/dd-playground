module.exports = {
  port: process.env.PORT || 3000,
  env: process.env.NODE_ENV || 'development',
  db: {
    url: process.env.DATABASE_URL || 'mongodb://localhost:27017/hybrid'
  },
  jwt: {
    secret: process.env.JWT_SECRET || 'default-secret'
  }
};