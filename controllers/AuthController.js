class AuthController {
  constructor(authService) {
    this.authService = authService;
  }

  async register(req, res) {
    try {
      const { email, password } = req.body;
      const user = await this.authService.register(email, password);
      const token = this.authService.generateToken(user.id);
      
      res.status(201).json({
        message: 'User registered successfully',
        user: user.toJSON(),
        token
      });
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }

  async login(req, res) {
    try {
      const { email, password } = req.body;
      const user = await this.authService.login(email, password);
      const token = this.authService.generateToken(user.id);
      
      res.json({
        message: 'Login successful',
        user: user.toJSON(),
        token
      });
    } catch (error) {
      res.status(401).json({ error: error.message });
    }
  }

  logout(req, res) {
    // With JWT, logout is handled client-side by removing the token
    // Server-side logout would require token blacklisting
    res.json({ message: 'Logout successful' });
  }
}

module.exports = AuthController;