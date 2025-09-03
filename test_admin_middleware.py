import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, g
from admin_middleware import AdminMiddleware

class TestAdminMiddleware(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.middleware = AdminMiddleware()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        self.app_context.pop()
    
    @patch('admin_middleware.request')
    def test_require_admin_no_token(self, mock_request):
        mock_request.headers.get.return_value = None
        
        @self.middleware.require_admin
        def dummy_route():
            return 'success'
        
        with self.app.test_request_context():
            response, status_code = dummy_route()
            self.assertEqual(status_code, 401)
            self.assertIn('Authorization token required', response.get_json()['error'])
    
    @patch('admin_middleware.request')
    @patch.object(AdminMiddleware, '__init__', lambda x: None)
    def test_require_admin_invalid_token(self, mock_request):
        middleware = AdminMiddleware()
        middleware.jwt_auth = MagicMock()
        middleware.jwt_auth.extract_token_from_header.return_value = 'invalid-token'
        middleware.jwt_auth.decode_token.return_value = None
        
        mock_request.headers.get.return_value = 'Bearer invalid-token'
        
        @middleware.require_admin
        def dummy_route():
            return 'success'
        
        with self.app.test_request_context():
            response, status_code = dummy_route()
            self.assertEqual(status_code, 401)
            self.assertIn('Invalid or expired token', response.get_json()['error'])
    
    @patch('admin_middleware.request')
    @patch.object(AdminMiddleware, '__init__', lambda x: None)
    def test_require_admin_non_admin_role(self, mock_request):
        middleware = AdminMiddleware()
        middleware.jwt_auth = MagicMock()
        middleware.jwt_auth.extract_token_from_header.return_value = 'valid-token'
        middleware.jwt_auth.decode_token.return_value = {
            'user_id': 1,
            'username': 'user',
            'role': 'user'
        }
        
        mock_request.headers.get.return_value = 'Bearer valid-token'
        
        @middleware.require_admin
        def dummy_route():
            return 'success'
        
        with self.app.test_request_context():
            response, status_code = dummy_route()
            self.assertEqual(status_code, 403)
            self.assertIn('Admin access required', response.get_json()['error'])
    
    @patch('admin_middleware.request')
    @patch.object(AdminMiddleware, '__init__', lambda x: None)
    def test_require_admin_success(self, mock_request):
        middleware = AdminMiddleware()
        middleware.jwt_auth = MagicMock()
        middleware.jwt_auth.extract_token_from_header.return_value = 'valid-token'
        middleware.jwt_auth.decode_token.return_value = {
            'user_id': 1,
            'username': 'admin',
            'role': 'admin'
        }
        
        mock_request.headers.get.return_value = 'Bearer valid-token'
        
        @middleware.require_admin
        def dummy_route():
            return 'success'
        
        with self.app.test_request_context():
            result = dummy_route()
            self.assertEqual(result, 'success')
            self.assertEqual(g.current_user['role'], 'admin')