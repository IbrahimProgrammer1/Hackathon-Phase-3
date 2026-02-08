import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch

from src.database import get_session
from main import app
from src.models.task_model import Task


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


def test_ownership_enforcement_get_tasks(client: TestClient, session: Session):
    """Test that users can only access their own tasks"""
    # Create tasks for different users
    task1 = Task(title="User 1 Task", description="Description", user_id="user_1")
    task2 = Task(title="User 2 Task", description="Description", user_id="user_2")
    session.add(task1)
    session.add(task2)
    session.commit()
    session.refresh(task1)
    session.refresh(task2)

    # Mock JWT token verification for user_1
    with patch('src.middleware.auth.JWTBearer.__call__') as mock_jwt:
        mock_jwt.return_value = "mock_token"

        # Mock request state to include user data for user_1
        with patch('src.api.tasks.request') as mock_request:
            mock_request.state.user = {"user_id": "user_1"}

            response = client.get("/api/user_1/tasks")

            assert response.status_code == 200
            data = response.json()
            # Should only return tasks for user_1
            assert len(data) == 1
            assert data[0]["id"] == task1.id


def test_ownership_enforcement_get_single_task(client: TestClient, session: Session):
    """Test that users can only access their own specific task"""
    # Create tasks for different users
    task1 = Task(title="User 1 Task", description="Description", user_id="user_1")
    task2 = Task(title="User 2 Task", description="Description", user_id="user_2")
    session.add(task1)
    session.add(task2)
    session.commit()
    session.refresh(task1)
    session.refresh(task2)

    # Mock JWT token verification for user_1
    with patch('src.middleware.auth.JWTBearer.__call__') as mock_jwt:
        mock_jwt.return_value = "mock_token"

        # Mock request state to include user data for user_1
        with patch('src.api.tasks.request') as mock_request:
            mock_request.state.user = {"user_id": "user_1"}

            # Try to access task that belongs to user_2
            response = client.get(f"/api/user_1/tasks/{task2.id}")

            # Should return 404 since task2 belongs to user_2, not user_1
            assert response.status_code == 404


def test_ownership_enforcement_update_task(client: TestClient, session: Session):
    """Test that users can only update their own tasks"""
    # Create tasks for different users
    task1 = Task(title="User 1 Task", description="Description", user_id="user_1")
    task2 = Task(title="User 2 Task", description="Description", user_id="user_2")
    session.add(task1)
    session.add(task2)
    session.commit()
    session.refresh(task1)
    session.refresh(task2)

    # Mock JWT token verification for user_1
    with patch('src.middleware.auth.JWTBearer.__call__') as mock_jwt:
        mock_jwt.return_value = "mock_token"

        # Mock request state to include user data for user_1
        with patch('src.api.tasks.request') as mock_request:
            mock_request.state.user = {"user_id": "user_1"}

            # Try to update task that belongs to user_2
            response = client.put(
                f"/api/user_1/tasks/{task2.id}",
                json={"title": "Updated Task", "description": "Updated Description"}
            )

            # Should return 404 since task2 belongs to user_2, not user_1
            assert response.status_code == 404


def test_ownership_enforcement_delete_task(client: TestClient, session: Session):
    """Test that users can only delete their own tasks"""
    # Create tasks for different users
    task1 = Task(title="User 1 Task", description="Description", user_id="user_1")
    task2 = Task(title="User 2 Task", description="Description", user_id="user_2")
    session.add(task1)
    session.add(task2)
    session.commit()
    session.refresh(task1)
    session.refresh(task2)

    # Mock JWT token verification for user_1
    with patch('src.middleware.auth.JWTBearer.__call__') as mock_jwt:
        mock_jwt.return_value = "mock_token"

        # Mock request state to include user data for user_1
        with patch('src.api.tasks.request') as mock_request:
            mock_request.state.user = {"user_id": "user_1"}

            # Try to delete task that belongs to user_2
            response = client.delete(f"/api/user_1/tasks/{task2.id}")

            # Should return 404 since task2 belongs to user_2, not user_1
            assert response.status_code == 404