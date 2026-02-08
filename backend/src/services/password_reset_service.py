from passlib.context import CryptContext
from datetime import datetime, timedelta
import secrets
from sqlmodel import Session, select
from ..models.task_model import PasswordResetToken, User
from fastapi import HTTPException, status

# Password context for hashing tokens
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def generate_reset_token() -> str:
    """Generate a secure random token for password reset"""
    return secrets.token_urlsafe(32)

def hash_token(token: str) -> str:
    """Hash the reset token for secure storage"""
    return pwd_context.hash(token)

def create_password_reset_token(user_id: str, session: Session) -> str:
    """Create a new password reset token for a user"""
    # First, invalidate any existing tokens for this user
    existing_tokens = session.exec(
        select(PasswordResetToken).where(
            PasswordResetToken.user_id == user_id,
            PasswordResetToken.used == False,
            PasswordResetToken.expires_at > datetime.utcnow()
        )
    ).all()

    for token in existing_tokens:
        token.used = True
        session.add(token)

    # Create a new token
    reset_token = generate_reset_token()
    token_hash = hash_token(reset_token)

    # Set expiration time (1 hour from now)
    expires_at = datetime.utcnow() + timedelta(hours=1)

    db_token = PasswordResetToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at
    )

    session.add(db_token)
    session.commit()

    return reset_token

def validate_reset_token_only(token: str, session: Session) -> str:
    """Validate a reset token without marking it as used - for UI validation"""
    token_hash = hash_token(token)

    db_token = session.exec(
        select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash
        )
    ).first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )

    if db_token.used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has already been used"
        )

    if db_token.expires_at < datetime.utcnow():
        # Mark as used to prevent reuse
        db_token.used = True
        session.add(db_token)
        session.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )

    # For validation only, don't mark as used
    return db_token.user_id


def verify_reset_token(token: str, session: Session) -> str:
    """Verify a reset token and return the associated user_id if valid, marking it as used"""
    token_hash = hash_token(token)

    db_token = session.exec(
        select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash
        )
    ).first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )

    if db_token.used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has already been used"
        )

    if db_token.expires_at < datetime.utcnow():
        # Mark as used to prevent reuse
        db_token.used = True
        session.add(db_token)
        session.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )

    # Mark token as used after successful verification
    db_token.used = True
    session.add(db_token)
    session.commit()

    return db_token.user_id