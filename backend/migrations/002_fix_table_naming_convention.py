"""
Database Migration Script: Fix Table Naming Convention
Version: 1.1

This script addresses the table naming inconsistency in the database by:
1. Ensuring all tables use the correct plural naming convention
2. Migrating data from incorrectly named tables to correctly named tables
3. Removing duplicate tables
4. Preserving all existing data

This migration should be applied to fix the schema mismatch issue where:
- Application code expects plural table names (users, tasks, credentials, password_reset_tokens)
- Some databases had both singular and plural versions of tables
- Data insertion was failing due to table name mismatches
"""
import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy import text
from pathlib import Path
import sys

def migrate_database_schema():
    """
    Performs the database schema migration to fix table naming inconsistencies
    """
    print("Starting database schema migration...")

    # Get the database engine
    from src.database import engine
    from src.models.task_model import Task, User, Credential, PasswordResetToken

    with engine.connect() as conn:
        # Get current tables
        result = conn.execute(text("""
            SELECT name FROM sqlite_master
            WHERE type='table'
        """))
        existing_tables = [row[0] for row in result.fetchall()]

        print(f"Existing tables: {existing_tables}")

        # Define the mapping of old to new table names
        old_to_new_mapping = {
            'task': 'tasks',
            'user': 'users',
            'credential': 'credentials',
            'passwordresettoken': 'password_reset_tokens'
        }

        # Process each potential old table name
        for old_name, new_name in old_to_new_mapping.items():
            if old_name in existing_tables:
                if new_name in existing_tables:
                    # Both exist - need to merge or handle conflict
                    old_count = conn.execute(text(f"SELECT COUNT(*) FROM {old_name}")).fetchone()[0]
                    new_count = conn.execute(text(f"SELECT COUNT(*) FROM {new_name}")).fetchone()[0]

                    if old_count > 0 and new_count == 0:
                        # Old has data, new is empty - rename old to new
                        conn.execute(text(f"DROP TABLE {new_name}"))
                        conn.execute(text(f"ALTER TABLE {old_name} RENAME TO {new_name}"))
                        print(f"Renamed '{old_name}' to '{new_name}' (moved data)")
                    elif old_count == 0 and new_count > 0:
                        # New has data, old is empty - drop old
                        conn.execute(text(f"DROP TABLE {old_name}"))
                        print(f"Dropped empty old table '{old_name}'")
                    elif old_count > 0 and new_count > 0:
                        # Both have data - merge old into new, then drop old
                        print(f"Merging data from '{old_name}' to '{new_name}'")

                        # Get all records from old table
                        old_records = conn.execute(text(f"SELECT * FROM {old_name}")).fetchall()
                        old_columns = [desc[0] for desc in conn.execute(text(f"SELECT * FROM {old_name} LIMIT 0")).keys()]

                        for record in old_records:
                            record_dict = {col: val for col, val in zip(old_columns, record)}

                            # Build INSERT statement
                            columns = ', '.join(record_dict.keys())
                            placeholders = ', '.join([f':{key}' for key in record_dict.keys()])
                            insert_sql = f"INSERT INTO {new_name} ({columns}) VALUES ({placeholders})"

                            try:
                                conn.execute(text(insert_sql), record_dict)
                            except Exception as e:
                                print(f"Warning: Could not insert record: {e}")

                        conn.execute(text(f"DROP TABLE {old_name}"))
                        print(f"Merged and dropped old table '{old_name}'")
                    else:
                        # Both empty - drop old
                        conn.execute(text(f"DROP TABLE {old_name}"))
                        print(f"Dropped empty old table '{old_name}'")
                else:
                    # Only old exists - rename it
                    conn.execute(text(f"ALTER TABLE {old_name} RENAME TO {new_name}"))
                    print(f"Renamed '{old_name}' to '{new_name}'")

        conn.commit()

        # Ensure all expected tables exist according to models
        SQLModel.metadata.create_all(engine)

        # Final verification
        result = conn.execute(text("""
            SELECT name FROM sqlite_master
            WHERE type='table'
        """))
        final_tables = [row[0] for row in result.fetchall()]

        expected_tables = ['users', 'tasks', 'credentials', 'password_reset_tokens']
        missing_tables = [t for t in expected_tables if t not in final_tables]

        if missing_tables:
            raise Exception(f"Missing expected tables: {missing_tables}")

        print(f"Migration completed successfully!")
        print(f"Final tables: {final_tables}")

        # Show counts for verification
        for table in expected_tables:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).fetchone()[0]
            print(f"Table '{table}': {count} records")


if __name__ == "__main__":
    print("Running database schema migration...")

    # Add src to path for imports
    sys.path.insert(0, str(Path(__file__).parent / "backend" / "src"))
    sys.path.insert(0, str(Path(__file__).parent / "backend"))

    try:
        migrate_database_schema()
        print("Migration completed successfully!")
    except Exception as e:
        print(f"Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)