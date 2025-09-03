const express = require('express');
const AuthService = require('./services/AuthService');
const UserStore = require('./storage/UserStore');
const createAuthRoutes = require('./routes/auth');

const app = express();
const userStore = new UserStore();
const authService = new AuthService(userStore);

app.use(express.json());
app.use('/auth', createAuthRoutes(authService));

// Protected route example
app.get('/profile', require('./middleware/auth')(authService), (req, res) => {
  const user = userStore.findById(req.userId);
  res.json({ user: user.toJSON() });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;