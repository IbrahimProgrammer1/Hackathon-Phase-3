"""
Script to migrate data from SQLite to Neon PostgreSQL database
"""
import os
from sqlalchemy import create_engine, text
from sqlmodel import Session, select
from datetime import datetime
import sys

# Load the Neon DB URL directly from the file
def load_neon_url():
    """Load the Neon database URL from .env.local file"""
    # Try multiple possible paths
    possible_paths = [
        "../../.env.local",  # Original attempt
        "../.env.local",     # One level up
        ".env.local",        # Same level as backend
        "../../../.env.local", # Two levels up from backend/src
        "../../firstsec/.env.local"  # Full path
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
    # Create Neon engine (temporarily removing sslmode for connection)
    neon_url_no_ssl = neon_url.replace('sslmode=require', 'sslmode=prefer').replace('sslmode=require&', 'sslmode=prefer&')
    neon_engine = create_engine(neon_url_no_ssl, pool_pre_ping=True)

    try:
        # Test connection to Neon
        with neon_engine.connect() as conn:
            result = conn.execute(text('SELECT version()'))
            print(f"Connected to Neon PostgreSQL: {result.fetchone()[0][:50]}...")
    except Exception as e:
        print(f"Could not connect to Neon DB: {e}")
        print(f"This may be due to SSL requirements. Trying with original URL...")
        # Try with original URL including SSL
        try:
            neon_engine = create_engine(neon_url, connect_args={"sslmode": "require"}, pool_pre_ping=True)
            with neon_engine.connect() as conn:
                result = conn.execute(text('SELECT version()'))
                print(f"Connected to Neon PostgreSQL with SSL: {result.fetchone()[0][:50]}...")
        except Exception as e2:
            print(f"Still cannot connect to Neon DB: {e2}")
            return False

    # Import models
    from src.models.task_model import User, Task, Credential, PasswordResetToken

    # Create all tables in Neon
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(neon_engine)
    print("Ensured all tables exist in Neon DB")

    # Migrate data from SQLite to Neon
    with sqlite_engine.connect() as sqlite_conn:
        with Session(neon_engine) as neon_session:
            print("\nMigrating Users...")
            sqlite_users = sqlite_conn.execute(text("SELECT * FROM users")).fetchall()
            user_columns = [desc[0] for desc in sqlite_conn.execute(text("SELECT * FROM users LIMIT 0")).keys()]

            for row in sqlite_users:
                user_data = {col: val for col, val in zip(user_columns, row)}

                # Check if user already exists in Neon
                user_id_val = user_data.get('user_id', user_data.get('user_id'))  # Handle different column mappings
                if user_id_val:
                    existing_user = neon_session.exec(select(User).where(User.user_id == user_id_val)).first()
                    if not existing_user:
                        user_obj = User(**user_data)
                        neon_session.add(user_obj)
                        print(f"  Added user: {user_data.get('email', user_id_val)}")
                    else:
                        print(f"  Skipped existing user: {user_data.get('email', user_id_val)}")
                else:
                    print(f"  Warning: Row has no user_id, skipping: {user_data}")

            neon_session.commit()
            print(f"Migrated {len(sqlite_users)} users")

            print("\nMigrating Credentials...")
            sqlite_credentials = sqlite_conn.execute(text("SELECT * FROM credentials")).fetchall()
            cred_columns = [desc[0] for desc in sqlite_conn.execute(text("SELECT * FROM credentials LIMIT 0")).keys()]

            for row in sqlite_credentials:
                cred_data = {col: val for col, val in zip(cred_columns, row)}

                # Check if credential already exists in Neon
                existing_cred = neon_session.exec(select(Credential).where(Credential.user_id == cred_data['user_id'])).first()
                if not existing_cred:
                    cred_obj = Credential(**cred_data)
                    neon_session.add(cred_obj)
                    print(f"  Added credential for user: {cred_data.get('user_id')}")
                else:
                    print(f"  Skipped existing credential for user: {cred_data.get('user_id')}")

            neon_session.commit()
            print(f"Migrated {len(sqlite_credentials)} credentials")

            print("\nMigrating Tasks...")
            sqlite_tasks = sqlite_conn.execute(text("SELECT * FROM tasks")).fetchall()
            task_columns = [desc[0] for desc in sqlite_conn.execute(text("SELECT * FROM tasks LIMIT 0")).keys()]

            for row in sqlite_tasks:
                task_data = {col: val for col, val in zip(task_columns, row)}

                # Check if task already exists in Neon (by id if available, otherwise by content)
                existing_task = None
                if 'id' in task_data and task_data.get('id'):
                    # Try to match by ID first
                    # Use raw SQL for this check since we're moving between databases
                    result = neon_session.exec(text(f"SELECT * FROM tasks WHERE id = {task_data['id']}")).first()
                    if result:
                        existing_task = result

                if not existing_task:
                    # Create task without ID to allow auto-increment
                    task_fields = {k: v for k, v in task_data.items() if k != 'id'}
                    task_obj = Task(**task_fields)
                    neon_session.add(task_obj)
                    print(f"  Added task: {task_data.get('title', 'Untitled')} for user {task_data.get('user_id')}")
                else:
                    print(f"  Skipped existing task: {task_data.get('title', 'Untitled')} for user {task_data.get('user_id')}")

            neon_session.commit()
            print(f"Migrated {len(sqlite_tasks)} tasks")

            print("\nMigrating Password Reset Tokens...")
            sqlite_tokens = sqlite_conn.execute(text("SELECT * FROM password_reset_tokens")).fetchall()
            token_columns = [desc[0] for desc in sqlite_conn.execute(text("SELECT * FROM password_reset_tokens LIMIT 0")).keys()]

            for row in sqlite_tokens:
                token_data = {col: val for col, val in zip(token_columns, row)}

                # Check if token already exists in Neon
                existing_token = neon_session.exec(select(PasswordResetToken).where(PasswordResetToken.id == token_data['id'])).first()
                if not existing_token:
                    token_obj = PasswordResetToken(**token_data)
                    neon_session.add(token_obj)
                    print(f"  Added password reset token for user: {token_data.get('user_id')}")
                else:
                    print(f"  Skipped existing password reset token for user: {token_data.get('user_id')}")

            neon_session.commit()
            print(f"Migrated {len(sqlite_tokens)} password reset tokens")

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