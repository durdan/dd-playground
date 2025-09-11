import unittest
from datetime import datetime
from repositories.user_repository import UserRepository
from services.user_service import UserService
from exceptions.user_exceptions import UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.repository = UserRepository()
        self.service = UserService(self.repository)
    
    def test_create_user_success(self):
        user = self.service.create_user("testuser", "test@example.com", "Password123")
        
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        self.assertIsInstance(user.created_at, datetime)
    
    def test_create_user_duplicate_email(self):
        self.service.create_user("user1", "test@example.com", "Password123")
        
        with self.assertRaises(UserAlreadyExistsError):
            self.service.create_user("user2", "test@example.com", "Password456")
    
    def test_create_user_weak_password(self):
        with self.assertRaises(ValueError) as context:
            self.service.create_user("testuser", "test@example.com", "weak")
        
        self.assertIn("Password must be at least 8 characters", str(context.exception))
    
    def test_authenticate_success(self):
        created_user = self.service.create_user("testuser", "test@example.com", "Password123")
        
        authenticated_user = self.service.authenticate("testuser", "Password123")
        self.assertEqual(authenticated_user.id, created_user.id)
        
        # Test with email
        authenticated_user = self.service.authenticate("test@example.com", "Password123")
        self.assertEqual(authenticated_user.id, created_user.id)
    
    def test_authenticate_invalid_credentials(self):
        self.service.create_user("testuser", "test@example.com", "Password123")
        
        with self.assertRaises(InvalidCredentialsError):
            self.service.authenticate("testuser", "wrongpassword")
    
    def test_authenticate_nonexistent_user(self):
        with self.assertRaises(InvalidCredentialsError):
            self.service.authenticate("nonexistent", "Password123")
    
    def test_get_user_not_found(self):
        with self.assertRaises(UserNotFoundError):
            self.service.get_user("nonexistent-id")
    
    def test_deactivate_user(self):
        user = self.service.create_user("testuser", "test@example.com", "Password123")
        
        deactivated_user = self.service.deactivate_user(user.id)
        self.assertFalse(deactivated_user.is_active)
        
        # Should not be able to authenticate deactivated user
        with self.assertRaises(InvalidCredentialsError):
            self.service.authenticate("testuser", "Password123")

class TestUserModel(unittest.TestCase):
    def test_invalid_email(self):
        from models.user import User
        
        with self.assertRaises(ValueError) as context:
            User("1", "testuser", "invalid-email", "hash", datetime.utcnow())
        
        self.assertIn("Invalid email format", str(context.exception))
    
    def test_short_username(self):
        from models.user import User
        
        with self.assertRaises(ValueError) as context:
            User("1", "ab", "test@example.com", "hash", datetime.utcnow())
        
        self.assertIn("Username must be at least 3 characters", str(context.exception))