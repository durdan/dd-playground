import unittest
import os
from config.database import DatabaseConfig

class TestDatabaseConfig(unittest.TestCase):
    
    def test_from_env_with_defaults(self):
        # Clear environment variables
        env_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
        original_values = {}
        for var in env_vars:
            original_values[var] = os.getenv(var)
            if var in os.environ:
                del os.environ[var]
        
        try:
            config = DatabaseConfig.from_env()
            self.assertEqual(config.host, 'localhost')
            self.assertEqual(config.port, 5432)
            self.assertEqual(config.database, 'user_management')
            self.assertEqual(config.username, 'postgres')
            self.assertEqual(config.password, 'password')
        finally:
            # Restore original values
            for var, value in original_values.items():
                if value is not None:
                    os.environ[var] = value
    
    def test_connection_string(self):
        config = DatabaseConfig(
            host='localhost',
            port=5432,
            database='testdb',
            username='testuser',
            password='testpass'
        )
        expected = "postgresql://testuser:testpass@localhost:5432/testdb"
        self.assertEqual(config.connection_string, expected)