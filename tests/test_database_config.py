import unittest
import os
import tempfile
import sqlite3
from database import DatabaseConfig, DatabaseError

class TestDatabaseConfig(unittest.TestCase):
    
    def setUp(self):
        """Create temporary database for testing."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_config = DatabaseConfig(self.temp_db.name)
    
    def tearDown(self):
        """Clean up temporary database."""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_database_creation(self):
        """Test database file is created."""
        self.assertTrue(os.path.exists(self.temp_db.name))
    
    def test_schema_initialization(self):
        """Test books table is created correctly."""
        self.db_config.initialize_schema()
        
        with self.db_config.get_connection() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='books'"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], 'books')
    
    def test_connection_context_manager(self):
        """Test connection context manager works properly."""
        self.db_config.initialize_schema()
        
        with self.db_config.get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM books")
            count = cursor.fetchone()[0]
            self.assertEqual(count, 0)
    
    def test_row_factory_enabled(self):
        """Test that row factory is enabled for dict-like access."""
        self.db_config.initialize_schema()
        
        with self.db_config.get_connection() as conn:
            conn.execute(
                "INSERT INTO books (title, author) VALUES (?, ?)",
                ("Test Book", "Test Author")
            )
            conn.commit()
            
            cursor = conn.execute("SELECT title, author FROM books LIMIT 1")
            row = cursor.fetchone()
            
            # Test dict-like access
            self.assertEqual(row['title'], "Test Book")
            self.assertEqual(row['author'], "Test Author")
    
    def test_drop_tables(self):
        """Test dropping tables functionality."""
        self.db_config.initialize_schema()
        self.db_config.drop_tables()
        
        with self.db_config.get_connection() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='books'"
            )
            result = cursor.fetchone()
            self.assertIsNone(result)
    
    def test_database_error_handling(self):
        """Test database error handling."""
        # Create invalid database path
        invalid_db = DatabaseConfig("/invalid/path/database.db")
        
        with self.assertRaises(DatabaseError):
            with invalid_db.get_connection() as conn:
                conn.execute("SELECT 1")

if __name__ == '__main__':
    unittest.main()