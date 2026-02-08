from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from uuid import uuid4
import os

from ..database import get_session
from ..models.task_model import User, Credential
from ..services.password_reset_service import create_password_reset_token, verify_reset_token, validate_reset_token_only
from ..services.email_service import email_service


router = APIRouter(prefix="/api/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-key-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 7


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


def _create_access_token(*, user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)
    payload = {"user_id": user_id, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
def register(data: RegisterRequest, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == data.email)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user_id = str(uuid4())

    user = User(user_id=user_id, email=data.email)
    session.add(user)
    session.commit()  # Commit user first to satisfy foreign key constraint

    # Now add the credential with the committed user_id
    cred = Credential(
        user_id=user_id,
        name=data.name,
        password_hash=pwd_context.hash(data.password),
    )
    session.add(cred)
    session.commit()

    token = _create_access_token(user_id=user_id)
    return {
        "token": token,
        "user": {
            "id": user_id,
            "email": user.email,
            "name": cred.name,
        },
    }


@router.post("/login")
def login(data: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    cred = session.exec(select(Credential).where(Credential.user_id == user.user_id)).first()
    if not cred:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not pwd_context.verify(data.password, cred.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = _create_access_token(user_id=user.user_id)
    return {
        "token": token,
        "user": {
            "id": user.user_id,
            "email": user.email,
            "name": cred.name,
        },
    }


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    password: str


class ValidateResetTokenRequest(BaseModel):
    token: str


@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    session: Session = Depends(get_session)
):
    # Find the user by email
    user = session.exec(select(User).where(User.email == data.email)).first()

    if not user:
        # Return success even if user doesn't exist to prevent email enumeration
        return {"message": "If an account with that email exists, a password reset link has been sent."}

    # Create a password reset token
    reset_token = create_password_reset_token(user.user_id, session)

    # Send the reset email
    email_sent = email_service.send_password_reset_email(data.email, reset_token)

    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send password reset email"
        )

    return {"message": "If an account with that email exists, a password reset link has been sent."}


@router.post("/reset-password")
def reset_password(
    data: ResetPasswordRequest,
    session: Session = Depends(get_session)
):
    # Verify the reset token and get the user_id
    user_id = verify_reset_token(data.token, session)

    # Get the user's credential to update the password
    credential = session.exec(
        select(Credential).where(Credential.user_id == user_id)
    ).first()

    if not credential:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user for reset token"
        )

    # Hash the new password
    new_password_hash = pwd_context.hash(data.password)

    # Update the password
    credential.password_hash = new_password_hash
    session.add(credential)
    session.commit()

    return {"message": "Password has been reset successfully"}


@router.post("/validate-reset-token")
def validate_reset_token(
    data: ValidateResetTokenRequest,
    session: Session = Depends(get_session)
):
    try:
        # This will raise an exception if the token is invalid
        # Using the validation-only function that doesn't mark the token as used
        user_id = validate_reset_token_only(data.token, session)

        # If we get here, the token is valid
        return {"valid": True, "message": "Token is valid"}
    except HTTPException:
        # If verification fails, re-raise the exception
        raise
