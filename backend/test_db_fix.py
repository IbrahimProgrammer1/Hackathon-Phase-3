"""
Test script to verify that the database fix works correctly
"""
import os
import sys
from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env.local'))

def test_database_connection():
    """Test that the application can connect and interact with the database"""
    try:
        from src.database import engine
        from src.models.task_model import Task, User, Credential, PasswordResetToken

        print("[TEST] Testing database connection and model mapping...")

        # Test 1: Verify that tables can be queried using the model classes
        with Session(engine) as session:
            # Count existing records
            user_count = session.exec(select(User)).all()
            task_count = session.exec(select(Task)).all()
            credential_count = session.exec(select(Credential)).all()
            token_count = session.exec(select(PasswordResetToken)).all()

            print(f"[SUCCESS] User records: {len(user_count)}")
            print(f"[SUCCESS] Task records: {len(task_count)}")
            print(f"[SUCCESS] Credential records: {len(credential_count)}")
            print(f"[SUCCESS] Password reset token records: {len(token_count)}")

            # Test 2: Try creating a new record
            from datetime import datetime
            from uuid import uuid4

            test_user_id = f"test-{str(uuid4())[:8]}"
            test_user = User(
                user_id=test_user_id,
                email=f"{test_user_id}@example.test",
                created_at=datetime.utcnow()
            )

            session.add(test_user)
            session.commit()
            print(f"[SUCCESS] Created test user: {test_user_id}")

            # Verify the record was created
            found_user = session.exec(select(User).where(User.user_id == test_user_id)).first()
            if found_user:
                print(f"[SUCCESS] Verified test user exists in database")

                # Clean up the test user
                session.delete(found_user)
                session.commit()
                print(f"[SUCCESS] Cleaned up test user")
            else:
                print(f"[ERROR] Could not verify test user in database")
                return False

        print("[SUCCESS] All database tests passed!")
        return True

    except Exception as e:
        print(f"[ERROR] Database test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("[TEST] Starting database functionality test...")

    # Add the src directory to Python path
    sys.path.insert(0, str(Path("src").resolve()))

    success = test_database_connection()

    if success:
        print("\n[SUCCESS] Database functionality test completed successfully!")
        print("[SUMMARY]:")
        print("   [OK] Models can access the database")
        print("   [OK] Correct table names are being used")
        print("   [OK] Data can be inserted and retrieved")
        print("   [OK] Database schema matches application expectations")
    else:
        print("\n[FAILURE] Database functionality test failed!")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)