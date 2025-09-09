import unittest
from datetime import datetime
from models import User, Organization, UserOrganization

class TestModels(unittest.TestCase):
    
    def test_user_creation_valid(self):
        user = User(1, "John Doe", "john@example.com", datetime.now())
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john@example.com")
    
    def test_user_creation_invalid_email(self):
        with self.assertRaises(ValueError):
            User(1, "John Doe", "invalid-email", datetime.now())
    
    def test_user_creation_empty_name(self):
        with self.assertRaises(ValueError):
            User(1, "", "john@example.com", datetime.now())
    
    def test_organization_creation_valid(self):
        org = Organization(1, "Tech Corp", "A tech company", datetime.now())
        self.assertEqual(org.name, "Tech Corp")
    
    def test_organization_creation_empty_name(self):
        with self.assertRaises(ValueError):
            Organization(1, "", "Description", datetime.now())

if __name__ == '__main__':
    unittest.main()