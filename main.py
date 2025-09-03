from database import DatabaseConfig, DatabaseError

def main():
    """Example usage of database configuration."""
    try:
        # Initialize database
        db_config = DatabaseConfig("example_books.db")
        db_config.initialize_schema()
        
        # Test connection
        with db_config.get_connection() as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print("Available tables:", [table[0] for table in tables])
            
        print("Database setup completed successfully!")
        
    except DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()