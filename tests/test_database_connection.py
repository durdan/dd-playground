import unittest
from unittest.mock import Mock, patch, MagicMock
from database.connection import DatabaseConnection
from config.database import DatabaseConfig

class TestDatabaseConnection(unittest.TestCase):
    
    def setUp(self):
        self.config = DatabaseConfig(
            host='localhost',
            port=5432,
            database='testdb',
            username='testuser',
            password='testpass'
        )
        self.db_conn = DatabaseConnection(self.config)
    
    @patch('psycopg2.pool.SimpleConnectionPool')
    def test_initialize_pool_success(self, mock_pool):
        mock_pool.return_value = Mock()
        
        self.db_conn.initialize_pool(min_connections=2, max_connections=5)
        
        mock_pool.assert_called_once_with(
            2, 5,
            host='localhost',
            port=5432,
            database='testdb',
            user='testuser',
            password='testpass'
        )
    
    @patch('psycopg2.pool.SimpleConnectionPool')
    def test_initialize_pool_failure(self, mock_pool):
        mock_pool.side_effect = Exception("Connection failed")
        
        with self.assertRaises(ConnectionError) as context:
            self.db_conn.initialize_pool()
        
        self.assertIn("Failed to create connection pool", str(context.exception))
    
    def test_get_connection_without_pool_raises_error(self):
        with self.assertRaises(RuntimeError) as context:
            with self.db_conn.get_connection():
                pass
        
        self.assertIn("Connection pool not initialized", str(context.exception))