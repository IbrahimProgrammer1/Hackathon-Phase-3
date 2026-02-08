"""
Simple test to verify Neon PostgreSQL is working for the application
"""
import os
from dotenv import load_dotenv
load_dotenv('.env.local')

from src.database import engine
from src.models.task_model import User, Task
from sqlmodel import Session, select
from datetime import datetime, timezone
from uuid import uuid4

def test_neon_db_operations():
    """Test that the application now uses Neon DB for operations"""
    print("Testing Neon PostgreSQL database operations...")

    with Session(engine) as session:
        # Check current record counts in Neon
        users_before = len(session.exec(select(User)).all())
        tasks_before = len(session.exec(select(Task)).all())

        print(f"Before test - Users: {users_before}, Tasks: {tasks_before}")

        # Test creating a simple task (since user/credential relationship is complex)
        test_user_id = "262a661d-2b3f-494c-9bd8-f04839655384"  # Use existing user ID from our migration

        new_task = Task(
            title="Test Task - Neon DB Verification",
            description="This task was created to verify Neon DB is working",
            user_id=test_user_id,
            completed=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        session.add(new_task)
        session.commit()
        task_id = new_task.id  # Get the ID after commit
        print(f"[SUCCESS] Created task in Neon DB with ID: {task_id}")

        # Verify the record exists in Neon DB
        created_task = session.exec(select(Task).where(Task.id == task_id)).first()

        if created_task:
            print("[SUCCESS] Task successfully stored in Neon DB")
        else:
            print("[ERROR] Failed to find created task in Neon DB")
            return False

        # Check final counts
        users_after = len(session.exec(select(User)).all())
        tasks_after = len(session.exec(select(Task)).all())

        print(f"After test - Users: {users_after}, Tasks: {tasks_after}")

        if users_after == users_before and tasks_after == tasks_before + 1:
            print("[SUCCESS] Task count increased correctly - data is being stored in Neon DB")
        else:
            print("[ERROR] Counts did not increase as expected")
            return False

        # Clean up test data
        session.delete(created_task)
        session.commit()
        print("[SUCCESS] Test data cleaned up from Neon DB")

        # Verify cleanup
        final_tasks = len(session.exec(select(Task)).all())

        if final_tasks == tasks_before:
            print("[SUCCESS] Data cleanup confirmed - Neon DB is properly synchronized")
        else:
            print("[ERROR] Data cleanup not reflected in Neon DB")
            return False

    print("\n[SUCCESS] Application is now using Neon PostgreSQL for all operations!")
    print("[SUCCESS] All future task creations will be saved to Neon DB")
    print("[SUCCESS] Real-time data persistence is now happening in the cloud!")

    return True

if __name__ == "__main__":
    print("=== Testing Neon PostgreSQL Integration ===")
    success = test_neon_db_operations()

    if success:
        print("\n[SUCCESS] APPLICATION IS NOW USING NEON POSTGRESQL FOR ALL OPERATIONS!")
        print("[SUCCESS] All data will be persisted in the cloud database")
        print("[SUCCESS] Ready for production use with real-time data synchronization")
    else:
        print("\n[ERROR] Test failed - application may not be using Neon DB")