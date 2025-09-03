import unittest
from datetime import datetime
from models.user import User
from repositories.user_repository import UserRepository
from services.user_service import UserService
from validators.user_validator import UserValidator
from exceptions import ValidationError, UserNotFoundError, UserAlreadyExistsError

class TestUserValidator(unittest.TestCase):
    def test_validate_create_success(self):
        data = {'name': 'John Doe', 'email': 'john@example.com'}
        UserValidator.validate_create(data)  # Should not raise
    
    def test_validate_create_missing_name(self):
        data = {'email': 'john@example.com'}
        with self.assertRaises(ValidationError):
            UserValidator.validate_create(data)
    
    def test_validate_create_invalid_email(self):
        data = {'name': 'John Doe', 'email': 'invalid-email'}
        with self.assertRaises(ValidationError):
            UserValidator.validate_create(data)

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.repo = UserRepository()
        self.user = User(0, 'John Doe', 'john@example.com', datetime.now())
    
    def test_create_user(self):
        created_user = self.repo.create(self.user)
        self.assertEqual(created_user.id, 1)
        self.assertEqual(created_user.name, 'John Doe')
    
    def test_create_duplicate_email(self):
        self.repo.create(self.user)
        duplicate_user = User(0, 'Jane Doe', 'john@example.com', datetime.now())
        with self.assertRaises(UserAlreadyExistsError):
            self.repo.create(duplicate_user)
    
    def test_get_user_not_found(self):
        with self.assertRaises(UserNotFoundError):
            self.repo.get_by_id(999)
    
    def test_delete_user(self):
        created_user = self.repo.create(self.user)
        self.repo.delete(created_user.id)
        with self.assertRaises(UserNotFoundError):
            self.repo.get_by_id(created_user.id)

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.repo = UserRepository()
        self.service = UserService(self.repo)
    
    def test_create_user_success(self):
        data = {'name': 'John Doe', 'email': 'john@example.com'}
        user = self.service.create_user(data)
        self.assertEqual(user.name, 'John Doe')
        self.assertEqual(user.email, 'john@example.com')
    
    def test_create_user_validation_error(self):
        data = {'name': '', 'email': 'john@example.com'}
        with self.assertRaises(ValidationError):
            self.service.create_user(data)
    
    def test_update_user_success(self):
        data = {'name': 'John Doe', 'email': 'john@example.com'}
        user = self.service.create_user(data)
        
        update_data = {'name': 'John Smith'}
        updated_user = self.service.update_user(user.id, update_data)
        self.assertEqual(updated_user.name, 'John Smith')
        self.assertEqual(updated_user.email, 'john@example.com')
    
    def test_get_all_users(self):
        self.service.create_user({'name': 'John', 'email': 'john@example.com'})
        self.service.create_user({'name': 'Jane', 'email': 'jane@example.com'})
        
        users = self.service.get_all_users()
        self.assertEqual(len(users), 2)

if __name__ == '__main__':
    unittest.main()