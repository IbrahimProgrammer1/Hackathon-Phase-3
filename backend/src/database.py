from sqlmodel import create_engine, Session
from typing import Generator
import os
from .models.task_model import Task, User, Credential, PasswordResetToken  # Import all models to register them with SQLModel

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_dev.db")

# Create the engine with additional connection parameters for PostgreSQL
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "sslmode": "require"  # Ensure SSL is used for PostgreSQL connections
        },
        pool_pre_ping=True  # Verify connections before use
    )
else:
    # For SQLite, use the standard engine
    engine = create_engine(DATABASE_URL)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Create database tables"""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)