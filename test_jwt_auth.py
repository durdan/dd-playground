import unittest
from datetime import datetime, timedelta
import jwt
from jwt_auth import JWTAuth
from config import Config

class TestJWTAuth(unittest.TestCase):
    def setUp(self):
        self.jwt_auth = JWTAuth()
    
    def test_generate_token_success(self):
        token = self.jwt_auth.generate_token(1, 'testuser', 'admin')
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 0)
    
    def test_generate_token_invalid_input(self):
        with self.assertRaises(ValueError):
            self.jwt_auth.generate_token(None, 'testuser', 'admin')
        
        with self.assertRaises(ValueError):
            self.jwt_auth.generate_token(1, '', 'admin')
    
    def test_decode_token_success(self):
        token = self.jwt_auth.generate_token(1, 'testuser', 'admin')
        payload = self.jwt_auth.decode_token(token)
        
        self.assertIsNotNone(payload)
        self.assertEqual(payload['user_id'], 1)
        self.assertEqual(payload['username'], 'testuser')
        self.assertEqual(payload['role'], 'admin')
    
    def test_decode_token_invalid(self):
        payload = self.jwt_auth.decode_token('invalid-token')
        self.assertIsNone(payload)
    
    def test_decode_token_expired(self):
        # Create expired token
        expired_payload = {
            'user_id': 1,
            'username': 'testuser',
            'role': 'admin',
            'exp': datetime.utcnow() - timedelta(hours=1)
        }
        expired_token = jwt.encode(expired_payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
        
        payload = self.jwt_auth.decode_token(expired_token)
        self.assertIsNone(payload)
    
    def test_extract_token_from_header(self):
        token = self.jwt_auth.extract_token_from_header('Bearer abc123')
        self.assertEqual(token, 'abc123')
        
        token = self.jwt_auth.extract_token_from_header('Invalid header')
        self.assertIsNone(token)
        
        token = self.jwt_auth.extract_token_from_header('')
        self.assertIsNone(token)