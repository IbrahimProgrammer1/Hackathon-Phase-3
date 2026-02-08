"""
Database index configuration for task model
"""
from sqlalchemy import Index, create_engine
from .models.task_model import Task
from .database import engine

def create_indexes():
    """Create database indexes for performance optimization"""
    # Create index for user_id to optimize user-based queries
    user_id_index = Index('idx_tasks_user_id', Task.user_id)
    user_id_index.create(engine, checkfirst=True)

    # Create index for completed field to optimize status-based queries
    completed_index = Index('idx_tasks_completed', Task.completed)
    completed_index.create(engine, checkfirst=True)

    print("Database indexes created successfully")