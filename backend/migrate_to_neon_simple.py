"""
Simple script to migrate data from SQLite to Neon PostgreSQL database
"""
import os
from sqlalchemy import create_engine, text
from sqlmodel import Session, select
import sys

def load_neon_url():
    """Load the Neon database URL from .env.local file"""
    # Try multiple possible paths
    possible_paths = [
        "../.env.local",     # One level up from backend
        ".env.local",        # Same level as backend
        "../../.env.local"   # Two levels up
    ]

    for env_file_path in possible_paths:
        if os.path.exists(env_file_path):
            print(f"Found .env.local at: {env_file_path}")
            with open(env_file_path, 'r') as f:
                for line in f:
                    if line.startswith("DATABASE_URL="):
                        url = line.split("=", 1)[1].strip()
                        # Remove any comments at the end
                        if "#" in url:
                            url = url.split("#")[0].strip()
                        return url
    print("Could not find .env.local in any expected location")
    return None

def migrate_data_to_neon():
    """Migrate all data from SQLite to Neon PostgreSQL"""
    print("Starting migration from SQLite to Neon PostgreSQL...")

    # Get Neon URL
    neon_url = load_neon_url()
    if not neon_url or not neon_url.startswith('postgresql'):
        print("ERROR: Could not find valid PostgreSQL URL in .env.local")
        return False

    print(f"Found Neon URL: {neon_url[:50]}...")

    # Source: SQLite database
    sqlite_engine = create_engine('sqlite:///./todo_dev.db')

    # Destination: Neon PostgreSQL database
    # Create Neon engine with SSL requirements
    neon_engine = create_engine(neon_url, connect_args={"sslmode": "require"}, pool_pre_ping=True)

    try:
        # Test connection to Neon
        with neon_engine.connect() as conn:
            result = conn.execute(text('SELECT version()'))
            print(f"Connected to Neon PostgreSQL: {result.fetchone()[0][:50]}...")
    except Exception as e:
        print(f"Could not connect to Neon DB: {e}")
        return False

    # Import models
    from src.models.task_model import User, Task, Credential, PasswordResetToken

    # Create all tables in Neon
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(neon_engine)
    print("Ensured all tables exist in Neon DB")

    # Get all data from SQLite and migrate to Neon
    with sqlite_engine.connect() as sqlite_conn:
        with Session(neon_engine) as neon_session:
            print("\nMigrating Users...")

            # Get users with proper column names
            sqlite_users = sqlite_conn.execute(text("SELECT user_id, email, created_at FROM users")).fetchall()
            users_added = 0

            for row in sqlite_users:
                user_id, email, created_at = row

                # Check if user already exists in Neon
                existing_user = neon_session.exec(select(User).where(User.user_id == user_id)).first()
                if not existing_user:
                    user_obj = User(user_id=user_id, email=email, created_at=created_at)
                    neon_session.add(user_obj)
                    print(f"  Added user: {email}")
                    users_added += 1
                else:
                    print(f"  Skipped existing user: {email}")

            neon_session.commit()
            print(f"Migrated {users_added} users")

            print("\nMigrating Credentials...")
            sqlite_credentials = sqlite_conn.execute(text("SELECT user_id, name, password_hash, created_at FROM credentials")).fetchall()
            creds_added = 0

            for row in sqlite_credentials:
                user_id, name, password_hash, created_at = row

                # Check if credential already exists in Neon
                existing_cred = neon_session.exec(select(Credential).where(Credential.user_id == user_id)).first()
                if not existing_cred:
                    cred_obj = Credential(user_id=user_id, name=name, password_hash=password_hash, created_at=created_at)
                    neon_session.add(cred_obj)
                    print(f"  Added credential for user: {user_id}")
                    creds_added += 1
                else:
                    print(f"  Skipped existing credential for user: {user_id}")

            neon_session.commit()
            print(f"Migrated {creds_added} credentials")

            print("\nMigrating Tasks...")
            sqlite_tasks = sqlite_conn.execute(text("SELECT title, description, completed, user_id, created_at, updated_at FROM tasks")).fetchall()
            tasks_added = 0

            for row in sqlite_tasks:
                title, description, completed, user_id, created_at, updated_at = row

                # Create task without specifying ID to allow auto-increment in PostgreSQL
                task_obj = Task(
                    title=title,
                    description=description,
                    completed=completed,
                    user_id=user_id,
                    created_at=created_at,
                    updated_at=updated_at
                )

                neon_session.add(task_obj)
                print(f"  Added task: {title} for user {user_id}")
                tasks_added += 1

            neon_session.commit()
            print(f"Migrated {tasks_added} tasks")

            print("\nMigrating Password Reset Tokens...")
            sqlite_tokens = sqlite_conn.execute(text("SELECT id, user_id, token_hash, expires_at, used, created_at FROM password_reset_tokens")).fetchall()
            tokens_added = 0

            for row in sqlite_tokens:
                id, user_id, token_hash, expires_at, used, created_at = row

                token_obj = PasswordResetToken(
                    id=id,
                    user_id=user_id,
                    token_hash=token_hash,
                    expires_at=expires_at,
                    used=used,
                    created_at=created_at
                )

                neon_session.add(token_obj)
                print(f"  Added password reset token for user: {user_id}")
                tokens_added += 1

            neon_session.commit()
            print(f"Migrated {tokens_added} password reset tokens")

    print("\nMigration completed successfully!")

    # Verify the data in Neon
    with Session(neon_engine) as session:
        users_count = len(session.exec(select(User)).all())
        tasks_count = len(session.exec(select(Task)).all())
        creds_count = len(session.exec(select(Credential)).all())
        tokens_count = len(session.exec(select(PasswordResetToken)).all())

        print(f"\nVerification - Neon DB contains:")
        print(f"  Users: {users_count}")
        print(f"  Tasks: {tasks_count}")
        print(f"  Credentials: {creds_count}")
        print(f"  Password Reset Tokens: {tokens_count}")

    return True

def main():
    print("=== Migrating Data to Neon PostgreSQL ===")

    success = migrate_data_to_neon()

    if success:
        print("\n[SUCCESS] Migration to Neon PostgreSQL completed successfully!")
        print("[SUCCESS] All data has been transferred from SQLite to Neon DB")
        print("[SUCCESS] Your application will now use Neon DB for all future operations")
    else:
        print("\n[ERROR] Migration failed!")
        return False

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)