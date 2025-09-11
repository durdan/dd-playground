import unittest
from datetime import datetime
from user import User

class TestUser(unittest.TestCase):
    """Test cases for User model."""
    
    def test_valid_user_creation(self):
        """Test creating a valid user."""
        user = User(id=1, email="test@example.com", name="John Doe")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.name, "John Doe")
        self.assertIsInstance(user.created_at, datetime)
    
    def test_email_normalization(self):
        """Test email is normalized to lowercase and trimmed."""
        user = User(id=1, email="  TEST@EXAMPLE.COM  ", name="John Doe")
        self.assertEqual(user.email, "test@example.com")
    
    def test_name_trimming(self):
        """Test name is trimmed."""
        user = User(id=1, email="test@example.com", name="  John Doe  ")
        self.assertEqual(user.name, "John Doe")
    
    def test_invalid_email_empty(self):
        """Test validation fails for empty email."""
        with self.assertRaises(ValueError) as context:
            User(id=1, email="", name="John Doe")
        self.assertIn("Email is required", str(context.exception))
    
    def test_invalid_email_format(self):
        """Test validation fails for invalid email format."""
        invalid_emails = ["invalid", "@example.com", "test@", "test.example.com"]
        for email in invalid_emails:
            with self.assertRaises(ValueError) as context:
                User(id=1, email=email, name="John Doe")
            self.assertIn("Invalid email format", str(context.exception))
    
    def test_invalid_name_empty(self):
        """Test validation fails for empty name."""
        with self.assertRaises(ValueError) as context:
            User(id=1, email="test@example.com", name="")
        self.assertIn("Name is required", str(context.exception))
    
    def test_invalid_name_too_short(self):
        """Test validation fails for name too short."""
        with self.assertRaises(ValueError) as context:
            User(id=1, email="test@example.com", name="A")
        self.assertIn("at least 2 characters", str(context.exception))
    
    def test_invalid_name_too_long(self):
        """Test validation fails for name too long."""
        long_name = "A" * 101
        with self.assertRaises(ValueError) as context:
            User(id=1, email="test@example.com", name=long_name)
        self.assertIn("less than 100 characters", str(context.exception))
    
    def test_invalid_email_type(self):
        """Test validation fails for non-string email."""
        with self.assertRaises(ValueError):
            User(id=1, email=123, name="John Doe")
    
    def test_invalid_name_type(self):
        """Test validation fails for non-string name."""
        with self.assertRaises(ValueError):
            User(id=1, email="test@example.com", name=123)