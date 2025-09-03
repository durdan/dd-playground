import sqlite3
import os
from contextlib import contextmanager
from typing import Optional

class DatabaseConfig:
    def __init__(self, db_path: str = "books.db"):
        self.db_path = db_path
        self._ensure_database_exists()
    
    def _ensure_database_exists(self) -> None:
        """Create database file if it doesn't exist."""
        if not os.path.exists(self.db_path):
            # Create empty file
            open(self.db_path, 'a').close()
    
    @contextmanager
    def get_connection(self):
        """Get database connection with automatic cleanup."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise DatabaseError(f"Database operation failed: {e}")
        finally:
            if conn:
                conn.close()
    
    def initialize_schema(self) -> None:
        """Create books table if it doesn't exist."""
        with self.get_connection() as conn:
            conn.execute(self._get_books_table_sql())
            conn.commit()
    
    def _get_books_table_sql(self) -> str:
        """Return SQL for creating books table."""
        return """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            publication_year INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    
    def drop_tables(self) -> None:
        """Drop all tables (useful for testing)."""
        with self.get_connection() as conn:
            conn.execute("DROP TABLE IF EXISTS books")
            conn.commit()

class DatabaseError(Exception):
    """Custom exception for database operations."""
    pass