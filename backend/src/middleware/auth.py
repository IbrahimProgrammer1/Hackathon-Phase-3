from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
import os
from sqlmodel import Session
from ..database import get_session
from ..models.task_model import User

# Get secret key from environment variable
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-key-change-in-production")
ALGORITHM = "HS256"


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme. Use 'Bearer <token>'"
                )
            token = credentials.credentials.strip()
            token_data = self.verify_jwt(token)
            if not token_data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token. Please log in again."
                )
            # Add user data to request for later use
            request.state.user = token_data
            return token
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No credentials provided."
            )

    def verify_jwt(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # Verify that the user_id exists in the payload
            user_id: str = payload.get("user_id")
            if user_id is None:
                return None
            return payload
        except jwt.ExpiredSignatureError:
            print(f"JWT Error: Token has expired")
            return None
        except jwt.JWTError as e:
            print(f"JWT Verification Error: {str(e)}")
            return None


def verify_token_owner(request: Request, path_user_id: str) -> bool:
    """
    Verify that the user_id in the JWT token matches the user_id in the path parameter
    This is critical for security to prevent users from accessing other users' data
    """
    if hasattr(request.state, 'user'):
        token_user_id = request.state.user.get('user_id')
        return token_user_id == path_user_id
    return False