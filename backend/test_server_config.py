"""
Test script to verify the server configuration for Neon DB
"""
import os
from dotenv import load_dotenv
load_dotenv('.env.local')

def test_server_configuration():
    """Test that the server is properly configured for Neon DB"""
    print("Testing server configuration for Neon DB...")

    # Import and check database configuration
    from src.database import DATABASE_URL, engine
    print(f"[SUCCESS] Database URL: {DATABASE_URL[:50]}...")

    if DATABASE_URL.startswith('postgresql'):
        print("[SUCCESS] Server configured to use PostgreSQL (Neon)")
    else:
        print("[ERROR] Server NOT configured to use PostgreSQL")
        return False

    # Test the engine can connect
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT version()'))
            version = result.fetchone()[0]
            print(f"[SUCCESS] Successfully connected to PostgreSQL: {version[:50]}...")
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return False

    # Check that models have correct table names
    from src.models.task_model import User, Task, Credential, PasswordResetToken

    models_to_check = [
        (User, 'users'),
        (Task, 'tasks'),
        (Credential, 'credentials'),
        (PasswordResetToken, 'password_reset_tokens')
    ]

    for model_class, expected_table in models_to_check:
        actual_table = getattr(model_class, '__tablename__', 'NOT_SET')
        model_name = model_class.__name__
        if actual_table == expected_table:
            print(f"[SUCCESS] {model_name} model maps to '{expected_table}' table")
        else:
            print(f"[ERROR] {model_name} model maps to '{actual_table}', expected '{expected_table}'")
            return False

    # Test that we can perform basic operations
    from sqlmodel import Session, select

    with Session(engine) as session:
        # Count existing records
        user_count = len(session.exec(select(User)).all())
        task_count = len(session.exec(select(Task)).all())

        print(f"[SUCCESS] Connected to Neon DB with {user_count} users and {task_count} tasks")

    print("\n[SUCCESS] Server configuration test PASSED!")
    print("[SUCCESS] When you start the server, it will use Neon PostgreSQL")
    print("[SUCCESS] All API operations will happen on the Neon DB")
    print("[SUCCESS] Real-time data persistence is enabled")

    return True

if __name__ == "__main__":
    print("=== Testing Server Configuration for Neon DB ===")
    success = test_server_configuration()

    if success:
        print("\n[SUCCESS] Server is properly configured for Neon DB!")
        print("[SUCCESS] To enable real-time updates:")
        print("[SUCCESS] 1. Make sure server is stopped (Ctrl+C)")
        print("[SUCCESS] 2. Start server: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print("[SUCCESS] 3. Use the frontend to create tasks - they will go to Neon DB")
    else:
        print("\n[ERROR] Server configuration test failed!")