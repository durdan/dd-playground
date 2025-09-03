import unittest
import os
from services.user_service import UserService
from repositories.user_repository import UserRepository
from models.user import UserValidationError

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_users.db"
        self.user_repository = UserRepository(self.test_db)
        self.user_service = UserService(self.user_repository)
    
    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_create_user_success(self):
        user = self.user_service.create_user("test@example.com", "Password123")
        
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "test@example.com")
        self.assertNotEqual(user.password_hash, "Password123")  # Should be hashed
    
    def test_create_user_invalid_email(self):
        with self.assertRaises(UserValidationError):
            self.user_service.create_user("invalid-email", "Password123")
    
    def test_create_user_duplicate_email(self):
        self.user_service.create_user("test@example.com", "Password123")
        
        with self.assertRaises(UserValidationError):
            self.user_service.create_user("test@example.com", "Password456")
    
    def test_authenticate_user_success(self):
        self.user_service.create_user("test@example.com", "Password123")
        
        user = self.user_service.authenticate_user("test@example.com", "Password123")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@example.com")
    
    def test_authenticate_user_wrong_password(self):
        self.user_service.create_user("test@example.com", "Password123")
        
        user = self.user_service.authenticate_user("test@example.com", "WrongPassword")
        self.assertIsNone(user)
    
    def test_change_password_success(self):
        user = self.user_service.create_user("test@example.com", "OldPassword123")
        
        success = self.user_service.change_password(user.id, "OldPassword123", "NewPassword123")
        self.assertTrue(success)
        
        # Verify old password no longer works
        auth_user = self.user_service.authenticate_user("test@example.com", "OldPassword123")
        self.assertIsNone(auth_user)
        
        # Verify new password works
        auth_user = self.user_service.authenticate_user("test@example.com", "NewPassword123")
        self.assertIsNotNone(auth_user)

if __name__ == '__main__':
    unittest.main()