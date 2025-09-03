import unittest
from models.user import User

class TestUserModel(unittest.TestCase):
    
    def test_valid_user_creation(self):
        user = User(
            email="test@example.com",
            password_hash="hashed_password_123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password_hash, "hashed_password_123")
        self.assertIsNone(user.id)
    
    def test_invalid_email_raises_error(self):
        with self.assertRaises(ValueError) as context:
            User(email="invalid-email", password_hash="hashed_password_123")
        self.assertIn("Invalid email format", str(context.exception))
    
    def test_empty_email_raises_error(self):
        with self.assertRaises(ValueError) as context:
            User(email="", password_hash="hashed_password_123")
        self.assertIn("Email is required", str(context.exception))
    
    def test_short_password_hash_raises_error(self):
        with self.assertRaises(ValueError) as context:
            User(email="test@example.com", password_hash="short")
        self.assertIn("Password hash too short", str(context.exception))
    
    def test_missing_password_hash_raises_error(self):
        with self.assertRaises(ValueError) as context:
            User(email="test@example.com", password_hash="")
        self.assertIn("Password hash is required", str(context.exception))