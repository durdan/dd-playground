import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from config.database import DatabaseConfig

class DatabaseConnection:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._pool = None
    
    def initialize_pool(self, min_connections=1, max_connections=10):
        """Initialize connection pool"""
        try:
            self._pool = psycopg2.pool.SimpleConnectionPool(
                min_connections,
                max_connections,
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password
            )
        except psycopg2.Error as e:
            raise ConnectionError(f"Failed to create connection pool: {e}")
    
    @contextmanager
    def get_connection(self):
        """Get connection from pool with automatic cleanup"""
        if not self._pool:
            raise RuntimeError("Connection pool not initialized")
        
        connection = None
        try:
            connection = self._pool.getconn()
            yield connection
        except psycopg2.Error as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                self._pool.putconn(connection)
    
    def close_pool(self):
        """Close all connections in pool"""
        if self._pool:
            self._pool.closeall()

# Global database instance
db_config = DatabaseConfig.from_env()
db = DatabaseConnection(db_config)