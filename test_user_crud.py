import unittest
from datetime import datetime
from models.user import User
from repositories.user_repository import UserRepository
from services.user_service import UserService
from exceptions import ValidationError, UserNotFoundError, UserAlreadyExistsError

class TestUserCRUD(unittest.TestCase):
    def setUp(self):
        self.repository = UserRepository()
        self.service = UserService(self.repository)
    
    def test_create_user_success(self):
        data = {'name': 'John Doe', 'email': 'john@example.com'}
        user = self.service.create_user(data)
        
        self.assertEqual(user.name, 'John Doe')
        self.assertEqual(user.email, 'john@example.com')
        self.assertEqual(user.id, 1)
        self.assertIsInstance(user.created_at, datetime)
    
    def test_create_user_invalid_name(self):
        data = {'name': '', 'email': 'john@example.com'}
        with self.assertRaises(ValidationError) as context:
            self.service.create_user(data)
        self.assertIn('Name is required', str(context.exception))
    
    def test_create_user_invalid_email(self):
        data = {'name': 'John Doe', 'email': 'invalid-email'}
        with self.assertRaises(ValidationError) as context:
            self.service.create_user(data)
        self.assertIn('Invalid email format', str(context.exception))
    
    def test_create_user_duplicate_email(self):
        data = {'name': 'John Doe', 'email': 'john@example.com'}
        self.service.create_user(data)
        
        with self.assertRaises(UserAlreadyExistsError):
            self.service.create_user(data)
    
    def test_get_user_success(self):
        data = {'name': 'John Doe', 'email': 'john@example.com'}
        created_user = self.service.create_user(data)
        
        retrieved_user = self.service.get_user(created_user.id)
        self.assertEqual(retrieved_user.name, 'John Doe')
        self.assertEqual(retrieved_user.email, 'john@example.com')
    
    def test_get_user_not_found(self):
        with self.assertRaises(UserNotFoundError):
            self.service.get_user(999)
    
    def test_get_all_users(self):
        data1 = {'name': 'John Doe', 'email': 'john@example.com'}
        data2 = {'name': 'Jane Smith', 'email': 'jane@example.com'}
        
        self.service.create_user(data1)
        self.service.create_user(data2)
        
        users = self.service.get_all_users()
        self.assertEqual(len(users), 2)
    
    def test_update_user_success(self):
        data = {'name': 'John Doe', 'email': 'john@example.com'}
        user = self.service.create_user(data)
        
        update_data = {'name': 'John Updated'}
        updated_user = self.service.update_user(user.id, update_data)
        
        self.assertEqual(updated_user.name, 'John Updated')
        self.assertEqual(updated_user.email, 'john@example.com')  # Unchanged
    
    def test_update_user_not_found(self):
        with self.assertRaises(UserNotFoundError):
            self.service.update_user(999, {'name': 'Test'})
    
    def test_update_user_duplicate_email(self):
        data1 = {'name': 'John Doe', 'email': 'john@example.com'}
        data2 = {'name': 'Jane Smith', 'email': 'jane@example.com'}
        
        user1 = self.service.create_user(data1)
        self.service.create_user(data2)
        
        with self.assertRaises(UserAlreadyExistsError):
            self.service.update_user(user1.id, {'email': 'jane@example.com'})
    
    def test_delete_user_success(self):
        data = {'name': 'John Doe', 'email': 'john@example.com'}
        user = self.service.create_user(data)
        
        self.service.delete_user(user.id)
        
        with self.assertRaises(UserNotFoundError):
            self.service.get_user(user.id)
    
    def test_delete_user_not_found(self):
        with self.assertRaises(UserNotFoundError):
            self.service.delete_user(999)

if __name__ == '__main__':
    unittest.main()