import unittest
from auth_service import AuthService

class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.auth_service = AuthService()
    
    def test_authenticate_success_admin(self):
        token = self.auth_service.authenticate('admin', 'admin123')
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
    
    def test_authenticate_success_user(self):
        token = self.auth_service.authenticate('user', 'user123')
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
    
    def test_authenticate_invalid_credentials(self):
        token = self.auth_service.authenticate('admin', 'wrongpassword')
        self.assertIsNone(token)
        
        token = self.auth_service.authenticate('nonexistent', 'password')
        self.assertIsNone(token)
    
    def test_authenticate_empty_credentials(self):
        with self.assertRaises(ValueError):
            self.auth_service.authenticate('', 'password')
        
        with self.assertRaises(ValueError):
            self.auth_service.authenticate('username', '')
    
    def test_get_user(self):
        user = self.auth_service.get_user('admin')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.role, 'admin')
        
        user = self.auth_service.get_user('nonexistent')
        self.assertIsNone(user)