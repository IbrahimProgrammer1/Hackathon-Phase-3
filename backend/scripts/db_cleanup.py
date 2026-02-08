"""
Database Cleanup Script for Todo Application

This script cleans up the duplicate table naming issue by:
1. Checking if both old (singular) and new (plural) tables exist
2. Renaming old tables to new names to match the application expectations
3. Dropping any remaining duplicate tables
"""

import os
import sys
from pathlib import Path
from sqlmodel import SQLModel, create_engine
from sqlalchemy import text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env.local'))

def get_database_url():
    """Get database URL from environment variable"""
    # Force use of SQLite for cleanup since that's where the dev data is
    return "sqlite:///./todo_dev.db"

def cleanup_duplicate_tables():
    """Drop old table names and ensure correct table names exist for the application"""
    try:
        database_url = get_database_url()
        print("[INFO] Starting database cleanup...")

        # Create engine
        engine = create_engine(database_url)

        # Import models to ensure they're registered with correct table names
        from src.models.task_model import Task, User, Credential, PasswordResetToken

        with engine.connect() as conn:
            # Check what tables currently exist (SQLite query)
            result = conn.execute(text("""
                SELECT name FROM sqlite_master
                WHERE type='table'
            """))

            existing_tables = [row[0] for row in result.fetchall()]
            print(f"[INFO] All existing tables: {existing_tables}")

            # Mapping of old (actual) table names to new (expected) table names
            old_to_expected_mapping = {
                'task': 'tasks',
                'user': 'users',
                'credential': 'credentials',
                'passwordresettoken': 'password_reset_tokens'
            }

            # Identify old tables that need to be dropped
            old_tables_to_drop = []
            for old_name in old_to_expected_mapping.keys():
                if old_name in existing_tables:
                    # Check if corresponding new table exists
                    new_name = old_to_expected_mapping[old_name]

                    if new_name in existing_tables:
                        # Both exist - check which has data and decide which to keep
                        old_count = conn.execute(text(f"SELECT COUNT(*) FROM {old_name}")).fetchone()[0]
                        new_count = conn.execute(text(f"SELECT COUNT(*) FROM {new_name}")).fetchone()[0]

                        if old_count > 0 and new_count == 0:
                            # Old has data, new is empty - drop new, rename old
                            conn.execute(text(f"DROP TABLE {new_name}"))
                            conn.execute(text(f"ALTER TABLE {old_name} RENAME TO {new_name}"))
                            conn.commit()
                            print(f"[SUCCESS] Renamed table '{old_name}' to '{new_name}' (moved data from old)")
                        elif old_count == 0 and new_count > 0:
                            # New has data, old is empty - just drop old
                            conn.execute(text(f"DROP TABLE {old_name}"))
                            conn.commit()
                            print(f"[SUCCESS] Dropped empty old table '{old_name}'")
                        elif old_count > 0 and new_count > 0:
                            # Both have data - this is a conflict, copy data from old to new then drop old
                            print(f"[INFO] Both '{old_name}' and '{new_name}' have data, merging...")

                            # Get all records from old table
                            old_records = conn.execute(text(f"SELECT * FROM {old_name}")).fetchall()
                            old_columns = [desc[0] for desc in conn.execute(text(f"SELECT * FROM {old_name} LIMIT 0")).keys()]

                            if old_records:
                                for record in old_records:
                                    # Convert record to dict
                                    record_dict = {col: val for col, val in zip(old_columns, record)}

                                    # Build INSERT statement
                                    columns = ', '.join(record_dict.keys())
                                    placeholders = ', '.join([f':{key}' for key in record_dict.keys()])  # Changed from %()s to :key for SQLite
                                    insert_sql = f"INSERT INTO {new_name} ({columns}) VALUES ({placeholders})"

                                    try:
                                        conn.execute(text(insert_sql), record_dict)
                                    except Exception as e:
                                        print(f"[WARNING] Could not insert record into {new_name}: {e}")

                                conn.commit()
                                print(f"[SUCCESS] Merged {len(old_records)} records from '{old_name}' to '{new_name}'")

                            # Drop the old table
                            conn.execute(text(f"DROP TABLE {old_name}"))
                            conn.commit()
                            print(f"[SUCCESS] Dropped merged old table '{old_name}'")
                        else:
                            # Both are empty - drop the old one
                            conn.execute(text(f"DROP TABLE {old_name}"))
                            conn.commit()
                            print(f"[SUCCESS] Dropped empty old table '{old_name}'")
                    else:
                        # Only old exists, rename it to new
                        conn.execute(text(f"ALTER TABLE {old_name} RENAME TO {new_name}"))
                        conn.commit()
                        print(f"[SUCCESS] Renamed table '{old_name}' to '{new_name}'")

            # Create any missing tables that weren't in the original database
            # This ensures all expected tables exist according to the model definitions
            SQLModel.metadata.create_all(engine)
            print("[INFO] Ensured all expected tables exist according to model definitions")

            # Final verification - check that expected tables exist
            result = conn.execute(text("""
                SELECT name FROM sqlite_master
                WHERE type='table'
                AND name IN ('task', 'user', 'credential', 'passwordresettoken', 'tasks', 'users', 'credentials', 'password_reset_tokens')
            """))

            remaining_tables = [row[0] for row in result.fetchall()]
            print(f"[INFO] Remaining potentially duplicate tables: {remaining_tables}")

            # Verify the expected tables exist and have the right names
            expected_tables = ['tasks', 'users', 'credentials', 'password_reset_tokens']
            missing_tables = []
            for table in expected_tables:
                if table not in existing_tables:
                    # Check if it exists after potential renames
                    result = conn.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name = '{table}'"))
                    if not result.fetchone():
                        missing_tables.append(table)

            if missing_tables:
                print(f"[ERROR] Expected tables are still missing after cleanup: {missing_tables}")
                return False

            print(f"[SUCCESS] Database cleanup completed successfully!")
            print(f"[SUCCESS] Tables now match application expectations: {expected_tables}")

            # Show final table counts
            for table in expected_tables:
                try:
                    count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).fetchone()
                    count = count_result[0] if count_result else 0
                    print(f"[INFO] Table '{table}' has {count} records")
                except Exception as e:
                    print(f"[ERROR] Could not query table '{table}': {e}")

            return True

    except Exception as e:
        print(f"[ERROR] Database cleanup failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main cleanup function"""
    print("[CLEANUP] Starting database cleanup process...")

    # Change to the backend directory if needed
    backend_dir = Path(".")
    os.chdir(backend_dir)
    print(f"[INFO] Current directory: {os.getcwd()}")

    # Add the src directory to Python path
    sys.path.insert(0, str(Path(".").resolve()))
    sys.path.insert(0, str(Path("src").resolve()))

    database_url = get_database_url()
    print(f"[INFO] Using database URL: {database_url.replace('@', '[REDACTED]@')[:50]}...")

    # Run cleanup
    if not cleanup_duplicate_tables():
        print("[ERROR] Database cleanup failed")
        return False

    print("\n[SUCCESS] Database cleanup completed successfully!")
    print("[SUMMARY]:")
    print("   [OK] Renamed tables from old singular names to new plural names")
    print("   [OK] Removed any duplicate tables")
    print("   [OK] Ensured all expected tables exist")
    print("   [OK] Application can now access the correct tables")

    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n[SUCCESS] Cleanup process completed successfully!")
        sys.exit(0)
    else:
        print("\n[FAILURE] Cleanup process failed!")
        sys.exit(1)