import unittest
from services.password_service import PasswordService

class TestPasswordService(unittest.TestCase):
    def setUp(self):
        self.password_service = PasswordService()
    
    def test_hash_password(self):
        password = "TestPassword123"
        hashed = self.password_service.hash_password(password)
        
        self.assertIsInstance(hashed, str)
        self.assertNotEqual(password, hashed)
        self.assertTrue(len(hashed) > 0)
    
    def test_verify_password_correct(self):
        password = "TestPassword123"
        hashed = self.password_service.hash_password(password)
        
        self.assertTrue(self.password_service.verify_password(password, hashed))
    
    def test_verify_password_incorrect(self):
        password = "TestPassword123"
        wrong_password = "WrongPassword123"
        hashed = self.password_service.hash_password(password)
        
        self.assertFalse(self.password_service.verify_password(wrong_password, hashed))

if __name__ == '__main__':
    unittest.main()