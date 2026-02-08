"""
Database Migration Script for Todo Application

This script handles the database setup and migration process for the Todo application.
It connects to the Neon database and creates the necessary tables and indexes.
"""

import os
import sys
from pathlib import Path
from sqlmodel import SQLModel, create_engine
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env.local'))

def get_database_url():
    """Get database URL from environment variable"""
    return os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/todo_db")

def test_connection(database_url):
    """Test the database connection"""
    try:
        # Extract database connection details for psycopg2
        # For this test, we'll use psycopg2 to test the connection
        import re

        # Updated regex to handle various PostgreSQL URL formats including Neon
        # This handles both standard format (with port) and Neon's format (without explicit port)
        # Pattern to handle both 'host:port' and just 'host' formats
        pattern = r'postgresql://([^:]+):([^@]+)@([^:/]+)(?::(\d+))?/([^?]+)'
        match = re.search(pattern, database_url)

        if not match:
            print(f"[ERROR] Invalid database URL format: {database_url}")
            return False

        username, password, host, port, database = match.groups()

        # If port is not specified in the URL, use default PostgreSQL port
        if port is None:
            port = '5432'

        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database
        )

        print(f"[SUCCESS] Successfully connected to database: {database} on {host}:{port}")
        conn.close()
        return True

    except Exception as e:
        print(f"[ERROR] Database connection failed: {str(e)}")
        return False

def create_tables():
    """Create all database tables using SQLModel"""
    try:
        database_url = get_database_url()
        print("[INFO] Creating database tables...")

        # Create engine
        engine = create_engine(database_url,
                              connect_args={
                                  "sslmode": "require"  # Ensure SSL is used for PostgreSQL connections
                              },
                              pool_pre_ping=True  # Verify connections before use
                             )

        # Import all models to ensure they're registered with SQLModel
        from src.models.task_model import Task, User, Credential, PasswordResetToken

        # Create all tables
        SQLModel.metadata.create_all(engine)
        print("[SUCCESS] Database tables created successfully!")

        return True

    except Exception as e:
        print(f"[ERROR] Failed to create tables: {str(e)}")
        return False

def create_indexes():
    """Create additional database indexes for performance"""
    try:
        database_url = get_database_url()
        print("[INFO] Creating database indexes...")

        engine = create_engine(database_url,
                              connect_args={
                                  "sslmode": "require"
                              },
                              pool_pre_ping=True
                             )

        from src.database_indexes import create_indexes as create_db_indexes
        create_db_indexes()
        print("[SUCCESS] Database indexes created successfully!")

        return True

    except Exception as e:
        # Indexes might already exist, which is fine
        error_msg = str(e).lower()
        if "duplicate" in error_msg or "already exists" in error_msg:
            print("[INFO] Database indexes already exist, continuing...")
            return True
        else:
            print(f"[ERROR] Failed to create indexes: {str(e)}")
            return False

def run_sql_migration_script():
    """Execute the SQL migration script"""
    try:
        script_path = Path("migrations/001_create_initial_schema.sql")
        if not script_path.exists():
            print(f"[WARNING] Migration script not found: {script_path}")
            return False

        print(f"[INFO] Running SQL migration script: {script_path}")

        # Read and execute the SQL script
        with open(script_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Connect and execute the script
        database_url = get_database_url()
        import re
        pattern = r'postgresql://([^:]+):([^@]+)@([^:/]+)(?::(\d+))?/([^?]+)'
        match = re.search(pattern, database_url)

        if not match:
            print(f"[ERROR] Invalid database URL format: {database_url}")
            return False

        username, password, host, port, database = match.groups()

        # If port is not specified in the URL, use default PostgreSQL port
        if port is None:
            port = '5432'

        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database
        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Execute the SQL script
        cursor.execute(sql_script)

        cursor.close()
        conn.close()

        print("[SUCCESS] SQL migration script executed successfully!")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to execute SQL migration script: {str(e)}")
        return False

def verify_schema():
    """Verify that all required tables exist"""
    try:
        database_url = get_database_url()
        engine = create_engine(database_url,
                              connect_args={
                                  "sslmode": "require"
                              },
                              pool_pre_ping=True
                             )

        from sqlalchemy import text

        # Check if all required tables exist
        tables_to_check = ['users', 'credentials', 'tasks', 'password_reset_tokens']

        with engine.connect() as conn:
            for table in tables_to_check:
                result = conn.execute(text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_schema = 'public'
                        AND table_name = :table_name
                    );
                """), {"table_name": table})

                exists = result.scalar()
                if exists:
                    print(f"[SUCCESS] Table '{table}' exists")
                else:
                    print(f"[ERROR] Table '{table}' does not exist")
                    return False

        print("[SUCCESS] All required tables exist!")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to verify schema: {str(e)}")
        return False

def main():
    """Main migration function"""
    print("[START] Starting database migration process...")

    # Change to the backend directory if needed
    backend_dir = Path(".")
    os.chdir(backend_dir)
    print(f"[INFO] Current directory: {os.getcwd()}")

    # Load environment variables again after changing directory
    load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env.local'))

    # Add the src directory to Python path
    sys.path.insert(0, str(Path(".").resolve()))
    sys.path.insert(0, str(Path("src").resolve()))

    database_url = get_database_url()
    print(f"[INFO] Using database URL: {database_url.replace('@', '[REDACTED]@')[:50]}...")

    # Test connection
    if not test_connection(database_url):
        print("[ERROR] Aborting migration due to connection failure")
        return False

    # Run the SQL migration script first
    if not run_sql_migration_script():
        print("[ERROR] Aborting migration due to SQL script failure")
        return False

    # Create tables using SQLModel
    if not create_tables():
        print("[ERROR] Aborting migration due to table creation failure")
        return False

    # Create additional indexes
    if not create_indexes():
        print("[ERROR] Aborting migration due to index creation failure")
        return False

    # Verify the schema
    if not verify_schema():
        print("[ERROR] Schema verification failed")
        return False

    print("\n[SUCCESS] Database migration completed successfully!")
    print("[SUMMARY]:")
    print("   [OK] Connection established")
    print("   [OK] Tables created")
    print("   [OK] Indexes created")
    print("   [OK] Schema verified")

    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n[SUCCESS] Migration process completed successfully!")
        sys.exit(0)
    else:
        print("\n[FAILURE] Migration process failed!")
        sys.exit(1)