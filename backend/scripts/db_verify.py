"""
Database Verification Script for Todo Application

This script verifies that the database is properly configured and accessible.
"""

import os
import sys
from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy import text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env.local'))

def get_database_url():
    """Get database URL from environment variable"""
    return os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/todo_db")

def test_basic_operations():
    """Test basic database operations"""
    try:
        database_url = get_database_url()
        print("[INFO] Testing database operations...")

        # Create engine
        engine = create_engine(database_url,
                              connect_args={
                                  "sslmode": "require"
                              },
                              pool_pre_ping=True
                             )

        # Import models
        from src.models.task_model import Task, User, Credential, PasswordResetToken

        with Session(engine) as session:
            # Test 1: Check if tables exist by trying a simple count query
            user_count = session.exec(select(User)).all()
            print(f"[SUCCESS] Users table accessible, found {len(user_count)} users")

            task_count = session.exec(select(Task)).all()
            print(f"[SUCCESS] Tasks table accessible, found {len(task_count)} tasks")

            # Test 2: Try creating a temporary test record (and immediately deleting it)
            from uuid import uuid4
            from datetime import datetime

            test_user_id = f"test-{str(uuid4())}"

            # Create a test user
            test_user = User(
                user_id=test_user_id,
                email=f"test-{test_user_id[:8]}@example.com",
                created_at=datetime.utcnow()
            )

            session.add(test_user)
            session.commit()
            print(f"[SUCCESS] Successfully created test user: {test_user_id[:8]}...")

            # Verify the user was created
            found_user = session.exec(select(User).where(User.user_id == test_user_id)).first()
            if found_user:
                print(f"[SUCCESS] Verified test user exists in database")
            else:
                print(f"[ERROR] Could not verify test user in database")
                return False

            # Clean up the test user
            session.delete(found_user)
            session.commit()
            print(f"[SUCCESS] Cleaned up test user")

        print("[SUCCESS] All basic operations test passed!")
        return True

    except Exception as e:
        print(f"[ERROR] Basic operations test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_connection_and_permissions():
    """Check database connection and permissions"""
    try:
        database_url = get_database_url()
        engine = create_engine(database_url,
                              connect_args={
                                  "sslmode": "require"
                              },
                              pool_pre_ping=True
                             )

        with engine.connect() as conn:
            # Test basic connectivity
            result = conn.execute(text("SELECT 1"))
            value = result.scalar()
            if value == 1:
                print("[SUCCESS] Basic connectivity test passed")
            else:
                print("[ERROR] Basic connectivity test failed")
                return False

            # Check if we can access table information
            result = conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name IN ('users', 'tasks', 'credentials', 'password_reset_tokens')
                ORDER BY table_name
            """))

            tables_found = [row[0] for row in result.fetchall()]
            print(f"[SUCCESS] Found tables in database: {', '.join(tables_found) if tables_found else 'None'}")

            # Check for any missing tables
            required_tables = {'users', 'tasks', 'credentials', 'password_reset_tokens'}
            found_tables = set(tables_found)
            missing_tables = required_tables - found_tables

            if missing_tables:
                print(f"[ERROR] Missing required tables: {missing_tables}")
                return False
            else:
                print("[SUCCESS] All required tables exist")

        return True

    except Exception as e:
        print(f"[ERROR] Connection and permissions test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main verification function"""
    print("[VERIFY] Starting database verification...")

    # Change to the backend directory if needed
    backend_dir = Path(".")
    os.chdir(backend_dir)
    print(f"[INFO] Current directory: {os.getcwd()}")

    # Add the src directory to Python path
    sys.path.insert(0, str(Path(".").resolve()))
    sys.path.insert(0, str(Path("src").resolve()))

    database_url = get_database_url()
    print(f"[INFO] Using database URL: {database_url.replace('@', '[REDACTED]@')[:50]}...")

    # Run connection and permissions check
    if not check_connection_and_permissions():
        print("[ERROR] Verification failed due to connection or permissions issue")
        return False

    # Run basic operations test
    if not test_basic_operations():
        print("[ERROR] Verification failed due to basic operations issue")
        return False

    print("\n[SUCCESS] Database verification completed successfully!")
    print("[SUMMARY]:")
    print("   [OK] Connection established")
    print("   [OK] All required tables exist")
    print("   [OK] Basic CRUD operations work")
    print("   [OK] Database permissions are correct")

    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n[SUCCESS] Verification process completed successfully!")
        sys.exit(0)
    else:
        print("\n[FAILURE] Verification process failed!")
        sys.exit(1)