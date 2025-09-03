import unittest
from datetime import datetime
from models.user import User
from validators.user_validator import UserValidator
from repositories.user_repository import UserRepository
from services.user_service import UserService
from exceptions import ValidationError, UserNotFoundError, UserAlreadyExistsError

class TestUserValidator(unittest.TestCase):
    def test_valid_create_data(self):
        data = {'name': 'John Doe', 'email': 'john@example.com'}
        UserValidator.validate_create(data)  # Should not raise
    
    def test_invalid_name(self):
        with self.assertRaises(ValidationError):
            UserValidator.validate_create({'name': '', 'email': 'john@example.com'})
    
    def test_invalid_email(self):
        with self.assertRaises(ValidationError):
            UserValidator.validate_create({'name': 'John', 'email': 'invalid-email'})

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.repo = UserRepository()
        self.user = User(0, 'John Doe', 'john@example.com', datetime.now())
    
    def test_create_user(self):
        created = self.repo.create(self.user)
        self.assertEqual(created.id, 1)
        self.assertEqual(created.name, 'John Doe')
    
    def test_create_duplicate_email(self):
        self.repo.create(self.user)
        duplicate = User(0, 'Jane Doe', 'john@example.com', datetime.now())
        with self.assertRaises(UserAlreadyExistsError):
            self.repo.create(duplicate)
    
    def test_get_user_not_found(self):
        with self.assertRaises(UserNotFoundError):
            self.repo.get_by_id(999)
    
    def test_update_user(self):
        created = self.repo.create(self.user)
        updated_user = User(created.id, 'Jane Doe', 'jane@example.com', created.created_at)
        result = self.repo.update(created.id, updated_user)
        self.assertEqual(result.name, 'Jane Doe')
    
    def test_delete_user(self):
        created = self.repo.create(self.user)
        self.repo.delete(created.id)
        with self.assertRaises(UserNotFoundError):
            self.repo.get_by_id(created.id)

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
    
    def test_update_user_partial(self):
        data = {'name': 'John Doe', 'email': 'john@example.com'}
        user = self.service.create_user(data)
        
        updated = self.service.update_user(user.id, {'name': 'Jane Doe'})
        self.assertEqual(updated.name, 'Jane Doe')
        self.assertEqual(updated.email, 'john@example.com')  # Unchanged
    
    def test_get_all_users(self):
        self.service.create_user({'name': 'John', 'email': 'john@example.com'})
        self.service.create_user({'name': 'Jane', 'email': 'jane@example.com'})
        
        users = self.service.get_all_users()
        self.assertEqual(len(users), 2)

if __name__ == '__main__':
    unittest.main()