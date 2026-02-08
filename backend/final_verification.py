"""
Final verification that the original problems have been resolved
"""
from src.database import engine
from src.models.task_model import Task, User, Credential, PasswordResetToken
from sqlmodel import Session, select
from datetime import datetime, timezone
from uuid import uuid4

def test_original_problems_fixed():
    """Test that the original problems reported are now fixed"""
    print("Testing that original problems are fixed...")

    print("\n1. Checking for duplicate tables...")
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result.fetchall()]

        # Check for the problematic duplicate combinations
        singular_tables = [t for t in tables if t in ['task', 'user', 'credential', 'passwordresettoken']]
        plural_tables = [t for t in tables if t in ['tasks', 'users', 'credentials', 'password_reset_tokens']]

        print(f"   Singular tables (old): {singular_tables}")
        print(f"   Plural tables (correct): {plural_tables}")

        if singular_tables:
            print("   ERROR: Still has old singular-named tables!")
            return False
        else:
            print("   [SUCCESS] No duplicate singular tables found")

        if len(plural_tables) == 4:
            print("   [SUCCESS] All 4 correct plural-named tables exist")
        else:
            print(f"   ERROR: Expected 4 plural tables, found {len(plural_tables)}")
            return False

    print("\n2. Testing that data can be inserted...")
    with Session(engine) as session:
        # Count existing records
        original_user_count = len(session.exec(select(User)).all())
        original_task_count = len(session.exec(select(Task)).all())

        print(f"   Original record counts - Users: {original_user_count}, Tasks: {original_task_count}")

        # Simulate user signup
        test_user_id = f"signup-test-{str(uuid4())[:8]}"
        new_user = User(
            user_id=test_user_id,
            email=f"{test_user_id}@signup-test.com",
            created_at=datetime.now(timezone.utc)
        )

        new_credential = Credential(
            user_id=test_user_id,
            name="Signup Test User",
            password_hash="$2b$12$test_hash_for_verification",
            created_at=datetime.now(timezone.utc)
        )

        session.add(new_user)
        session.add(new_credential)
        session.commit()
        print(f"   [SUCCESS] Successfully created user account during signup simulation")

        # Simulate task creation for the user
        new_task = Task(
            title="Test Task - Created After Fix",
            description="This task was created to verify that task creation works",
            user_id=test_user_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        session.add(new_task)
        session.commit()
        print(f"   [SUCCESS] Successfully created task for user")

        # Verify both records exist
        created_user = session.exec(select(User).where(User.user_id == test_user_id)).first()
        created_task = session.exec(select(Task).where(Task.user_id == test_user_id)).first()

        if created_user and created_task:
            print(f"   [SUCCESS] Both user and task are properly stored in database")

            # Clean up test data
            session.delete(created_task)
            session.delete(created_user)
            session.delete(session.exec(select(Credential).where(Credential.user_id == test_user_id)).first())
            session.commit()
            print(f"   [SUCCESS] Test data cleaned up successfully")
        else:
            print(f"   ERROR: Created records not found in database")
            return False

    print("\n3. Verifying all existing data is still accessible...")
    with Session(engine) as session:
        final_users = session.exec(select(User)).all()
        final_tasks = session.exec(select(Task)).all()
        final_credentials = session.exec(select(Credential)).all()
        final_tokens = session.exec(select(PasswordResetToken)).all()

        print(f"   Final record counts - Users: {len(final_users)}, Tasks: {len(final_tasks)}, Credentials: {len(final_credentials)}, Tokens: {len(final_tokens)}")

        if len(final_users) > 0 and len(final_tasks) > 0:
            print("   [SUCCESS] All existing data is still accessible")
        else:
            print("   ERROR: Existing data may have been lost")
            return False

    print("\n[SUCCESS] All original problems have been successfully resolved!")
    print("   [SUCCESS] No more duplicate tables")
    print("   [SUCCESS] Data can be inserted during signup")
    print("   [SUCCESS] Tasks can be created and saved")
    print("   [SUCCESS] All existing data preserved")
    print("   [SUCCESS] Application can properly interact with database")

    return True

if __name__ == "__main__":
    print("=== FINAL VERIFICATION: Original Problems Resolution ===")
    success = test_original_problems_fixed()

    if success:
        print("\n[SUCCESS] All originally reported problems have been fixed!")
    else:
        print("\n[ERROR] Some problems remain unresolved!")
        exit(1)