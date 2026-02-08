import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch

from src.database import get_session
from main import app


# Override the database session for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_jwt_verification_middleware(client: TestClient):
    """Test that JWT verification middleware works correctly"""
    # Test without token
    response = client.get("/api/test_user_123/tasks")
    assert response.status_code in [401, 403]  # Should be unauthorized without token

    # Test with invalid token
    response = client.get(
        "/api/test_user_123/tasks",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code in [401, 403]  # Should be unauthorized with invalid token


def test_jwt_verification_with_valid_token(client: TestClient):
    """Test that JWT verification works with a valid token"""
    # Mock JWT token verification
    with patch('src.middleware.auth.JWTBearer.__call__') as mock_jwt:
        mock_jwt.return_value = "mock_token"

        # Mock request state to include user data
        with patch('src.api.tasks.request') as mock_request:
            mock_request.state.user = {"user_id": "test_user_123"}

            response = client.get(
                "/api/test_user_123/tasks",
                headers={"Authorization": "Bearer valid_token"}
            )

            # Should succeed with valid token
            assert response.status_code == 200