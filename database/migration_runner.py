import os
from database.connection import db

def run_migrations():
    """Run all migration files"""
    migrations_dir = 'migrations'
    
    if not os.path.exists(migrations_dir):
        raise FileNotFoundError(f"Migrations directory '{migrations_dir}' not found")
    
    migration_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.sql')])
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        for migration_file in migration_files:
            print(f"Running migration: {migration_file}")
            
            with open(os.path.join(migrations_dir, migration_file), 'r') as f:
                migration_sql = f.read()
            
            try:
                cursor.execute(migration_sql)
                conn.commit()
                print(f"✓ Migration {migration_file} completed")
            except Exception as e:
                conn.rollback()
                raise RuntimeError(f"Migration {migration_file} failed: {e}")

if __name__ == "__main__":
    db.initialize_pool()
    try:
        run_migrations()
    finally:
        db.close_pool()