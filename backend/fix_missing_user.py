"""
Script to fix the missing user issue in Neon DB
"""
import os
from dotenv import load_dotenv
load_dotenv('.env.local')

from src.database import engine
from src.models.task_model import User, Credential
from sqlmodel import Session, select
from datetime import datetime, timezone

def fix_missing_user():
    """Add the missing user to Neon DB to fix foreign key constraint"""
    missing_user_id = '4cd9b081-586d-4670-8f4d-619e7e842198'

    print(f"Attempting to fix missing user: {missing_user_id}")

    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.user_id == missing_user_id)).first()

        if existing_user:
            print(f"User {missing_user_id} already exists in Neon DB")
            return True

        # Add user first
        new_user = User(
            user_id=missing_user_id,
            email='frontend-user@example.com',  # Placeholder email
            created_at=datetime.now(timezone.utc)
        )

        session.add(new_user)
        session.commit()  # Commit user first to satisfy foreign key constraint
        print(f"Added user {missing_user_id} to Neon DB")

        # Now add the credential
        new_credential = Credential(
            user_id=missing_user_id,
            name='Frontend User',
            password_hash='$2b$12$placeholder_hash_for_migration',  # Placeholder hash
            created_at=datetime.now(timezone.utc)
        )

        session.add(new_credential)
        session.commit()
        print(f"Added credential for user {missing_user_id} to Neon DB")

    print("[SUCCESS] Missing user has been added to Neon DB!")
    print("[SUCCESS] Foreign key constraint issue is now resolved!")
    print("[SUCCESS] You can now create tasks for this user!")

    # Verify the user exists
    with Session(engine) as session:
        user = session.exec(select(User).where(User.user_id == missing_user_id)).first()
        if user:
            print(f"[SUCCESS] Verification: User {missing_user_id} exists in Neon DB")
        else:
            print(f"[ERROR] Verification: User {missing_user_id} still does not exist")
            return False

    return True

if __name__ == "__main__":
    print("=== Fixing Missing User in Neon DB ===")
    success = fix_missing_user()

    if success:
        print("\n[SUCCESS] The missing user has been added to Neon DB!")
        print("[SUCCESS] You can now create tasks for this user!")
        print("[SUCCESS] The foreign key constraint error is resolved!")
    else:
        print("\n[ERROR] Failed to fix the missing user issue!")