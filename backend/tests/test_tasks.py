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


def test_create_task(client: TestClient):
    """Test creating a new task"""
    # Mock JWT token verification
    with patch('src.middleware.auth.JWTBearer.__call__') as mock_jwt:
        mock_jwt.return_value = "mock_token"

        # Mock request state to include user data
        with patch('src.api.tasks.request') as mock_request:
            mock_request.state.user = {"user_id": "test_user_123"}

            response = client.post(
                "/api/test_user_123/tasks",
                json={"title": "Test Task", "description": "Test Description"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "Test Task"
            assert data["description"] == "Test Description"
            assert data["completed"] is False


def test_get_tasks(client: TestClient):
    """Test getting all tasks for a user"""
    # Mock JWT token verification
    with patch('src.middleware.auth.JWTBearer.__call__') as mock_jwt:
        mock_jwt.return_value = "mock_token"

        # Mock request state to include user data
        with patch('src.api.tasks.request') as mock_request:
            mock_request.state.user = {"user_id": "test_user_123"}

            response = client.get("/api/test_user_123/tasks")

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)


def test_get_single_task(client: TestClient, session: Session):
    """Test getting a single task"""
    # Create a task in the database
    task = Task(title="Test Task", description="Test Description", user_id="test_user_123")
    session.add(task)
    session.commit()
    session.refresh(task)

    # Mock JWT token verification
    with patch('src.middleware.auth.JWTBearer.__call__') as mock_jwt:
        mock_jwt.return_value = "mock_token"

        # Mock request state to include user data
        with patch('src.api.tasks.request') as mock_request:
            mock_request.state.user = {"user_id": "test_user_123"}

            response = client.get(f"/api/test_user_123/tasks/{task.id}")

            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "Test Task"


def test_update_task(client: TestClient, session: Session):
    """Test updating a task"""
    # Create a task in the database
    task = Task(title="Original Task", description="Original Description", user_id="test_user_123")
    session.add(task)
    session.commit()
    session.refresh(task)

    # Mock JWT token verification
    with patch('src.middleware.auth.JWTBearer.__call__') as mock_jwt:
        mock_jwt.return_value = "mock_token"

        # Mock request state to include user data
        with patch('src.api.tasks.request') as mock_request:
            mock_request.state.user = {"user_id": "test_user_123"}

            response = client.put(
                f"/api/test_user_123/tasks/{task.id}",
                json={"title": "Updated Task", "description": "Updated Description"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "Updated Task"


def test_delete_task(client: TestClient, session: Session):
    """Test deleting a task"""
    # Create a task in the database
    task = Task(title="Task to Delete", description="Description", user_id="test_user_123")
    session.add(task)
    session.commit()
    session.refresh(task)

    # Mock JWT token verification
    with patch('src.middleware.auth.JWTBearer.__call__') as mock_jwt:
        mock_jwt.return_value = "mock_token"

        # Mock request state to include user data
        with patch('src.api.tasks.request') as mock_request:
            mock_request.state.user = {"user_id": "test_user_123"}

            response = client.delete(f"/api/test_user_123/tasks/{task.id}")

            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Task deleted successfully"