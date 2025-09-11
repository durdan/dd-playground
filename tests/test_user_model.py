import unittest
from datetime import datetime
from models.user import User

class TestUserModel(unittest.TestCase):
    
    def test_valid_user_creation(self):
        user = User(id=1, username="testuser", email="test@example.com", password_hash="hash123")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        self.assertIsInstance(user.created_at, datetime)
    
    def test_user_creation_with_custom_created_at(self):
        custom_time = datetime(2023, 1, 1)
        user = User(id=1, username="testuser", email="test@example.com", 
                   password_hash="hash123", created_at=custom_time)
        self.assertEqual(user.created_at, custom_time)
    
    def test_invalid_username_empty(self):
        with self.assertRaises(ValueError) as context:
            User(id=1, username="", email="test@example.com", password_hash="hash123")
        self.assertIn("Username must be at least 3 characters", str(context.exception))
    
    def test_invalid_username_too_short(self):
        with self.assertRaises(ValueError):
            User(id=1, username="ab", email="test@example.com", password_hash="hash123")
    
    def test_invalid_username_whitespace_only(self):
        with self.assertRaises(ValueError):
            User(id=1, username="   ", email="test@example.com", password_hash="hash123")
    
    def test_invalid_email_empty(self):
        with self.assertRaises(ValueError) as context:
            User(id=1, username="testuser", email="", password_hash="hash123")
        self.assertIn("Invalid email format", str(context.exception))
    
    def test_invalid_email_format(self):
        invalid_emails = ["invalid", "@example.com", "test@", "test.example.com", "test@.com"]
        for email in invalid_emails:
            with self.assertRaises(ValueError):
                User(id=1, username="testuser", email=email, password_hash="hash123")
    
    def test_valid_email_formats(self):
        valid_emails = ["test@example.com", "user.name@domain.co.uk", "test+tag@example.org"]
        for email in valid_emails:
            user = User(id=1, username="testuser", email=email, password_hash="hash123")
            self.assertEqual(user.email, email)
    
    def test_empty_password_hash(self):
        with self.assertRaises(ValueError) as context:
            User(id=1, username="testuser", email="test@example.com", password_hash="")
        self.assertIn("Password hash cannot be empty", str(context.exception))