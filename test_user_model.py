import unittest
from datetime import datetime
from models.user import User, UserValidator, UserValidationError

class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User(email="test@example.com", password_hash="hashed_password")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password_hash, "hashed_password")
        self.assertIsInstance(user.created_at, datetime)

class TestUserValidator(unittest.TestCase):
    def test_valid_email(self):
        # Should not raise exception
        UserValidator.validate_email("test@example.com")
    
    def test_invalid_email(self):
        with self.assertRaises(UserValidationError):
            UserValidator.validate_email("invalid-email")
        
        with self.assertRaises(UserValidationError):
            UserValidator.validate_email("")
    
    def test_valid_password(self):
        # Should not raise exception
        UserValidator.validate_password("Password123")
    
    def test_invalid_password(self):
        with self.assertRaises(UserValidationError):
            UserValidator.validate_password("short")  # Too short
        
        with self.assertRaises(UserValidationError):
            UserValidator.validate_password("nouppercase123")  # No uppercase
        
        with self.assertRaises(UserValidationError):
            UserValidator.validate_password("NOLOWERCASE123")  # No lowercase
        
        with self.assertRaises(UserValidationError):
            UserValidator.validate_password("NoDigits")  # No digits

if __name__ == '__main__':
    unittest.main()