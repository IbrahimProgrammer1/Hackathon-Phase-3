from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timedelta
import uuid


class TaskBase(SQLModel):
    title: str = Field(min_length=1)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: str = Field(primary_key=True, index=True)
    email: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Credential(SQLModel, table=True):
    __tablename__ = "credentials"
    user_id: str = Field(primary_key=True, index=True)
    name: Optional[str] = Field(default=None)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PasswordResetToken(SQLModel, table=True):
    __tablename__ = "password_reset_tokens"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)
    token_hash: str  # Store hash of the token for security
    expires_at: datetime
    used: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
