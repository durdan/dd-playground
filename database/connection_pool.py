import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import threading
import time

class DatabasePool:
    def __init__(self, database_url: str, min_conn: int = 5, max_conn: int = 20):
        self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
            min_conn, max_conn, database_url
        )
        self.stats = {
            'total_queries': 0,
            'slow_queries': 0,
            'avg_response_time': 0
        }
        self._lock = threading.Lock()
    
    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = self.connection_pool.getconn()
            yield conn
        finally:
            if conn:
                self.connection_pool.putconn(conn)
    
    @contextmanager
    def get_cursor(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                cursor.close()
    
    def execute_query(self, query: str, params=None):
        start_time = time.time()
        
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        
        execution_time = (time.time() - start_time) * 1000
        
        # Update stats
        with self._lock:
            self.stats['total_queries'] += 1
            if execution_time > 200:  # Slow query threshold
                self.stats['slow_queries'] += 1
            
            # Update rolling average
            current_avg = self.stats['avg_response_time']
            total_queries = self.stats['total_queries']
            self.stats['avg_response_time'] = (
                (current_avg * (total_queries - 1) + execution_time) / total_queries
            )
        
        return result, execution_time