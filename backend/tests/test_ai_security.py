"""
Test Suite for AI Security - JWT Propagation and Ownership

Tests T039: Security test for create_task JWT propagation
Tests that JWT is properly attached and user_id is derived from JWT.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from unittest.mock import Mock, patch, MagicMock
from ai.tool_executor import ToolExecutor
import httpx


class TestCreateTaskJWTPropagation:
    """T039: Test create_task JWT propagation and security"""

    def test_jwt_attached_to_create_task_request(self):
        """Test that JWT is attached to Authorization header"""
        executor = ToolExecutor(jwt="test-jwt-token", user_id="test-user")

        # Verify JWT is in client headers
        assert "Authorization" in executor.client.headers
        assert executor.client.headers["Authorization"] == "Bearer test-jwt-token"

        executor.close()

    def test_user_id_derived_from_jwt_not_parameters(self):
        """Test that user_id comes from JWT, not tool parameters"""
        executor = ToolExecutor(jwt="test-jwt-token", user_id="alice")

        with patch.object(executor.client, 'post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "id": 1,
                "user_id": "alice",  # Should match JWT user_id
                "title": "Test Task",
                "description": None,
                "completed": False,
                "created_at": "2026-02-16T12:00:00Z",
                "updated_at": "2026-02-16T12:00:00Z"
            }
            mock_post.return_value = mock_response

            # Execute tool - note that parameters don't include user_id
            result = executor.execute_tool("create_task", {
                "title": "Test Task"
            })

            # Verify API was called with correct user_id in URL
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            assert "/api/alice/tasks" in call_args[0][0]

            # Verify result has correct user_id
            assert result["success"]
            assert result["result"]["user_id"] == "alice"

        executor.close()

    def test_different_users_isolated(self):
        """Test that different users' requests are isolated"""
        # User Alice
        executor_alice = ToolExecutor(jwt="alice-jwt", user_id="alice")

        with patch.object(executor_alice.client, 'post') as mock_post_alice:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "id": 1,
                "user_id": "alice",
                "title": "Alice's Task",
                "description": None,
                "completed": False,
                "created_at": "2026-02-16T12:00:00Z",
                "updated_at": "2026-02-16T12:00:00Z"
            }
            mock_post_alice.return_value = mock_response

            result_alice = executor_alice.execute_tool("create_task", {
                "title": "Alice's Task"
            })

            # Verify Alice's request used her user_id
            call_args = mock_post_alice.call_args
            assert "/api/alice/tasks" in call_args[0][0]
            assert result_alice["result"]["user_id"] == "alice"

        executor_alice.close()

        # User Bob
        executor_bob = ToolExecutor(jwt="bob-jwt", user_id="bob")

        with patch.object(executor_bob.client, 'post') as mock_post_bob:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "id": 2,
                "user_id": "bob",
                "title": "Bob's Task",
                "description": None,
                "completed": False,
                "created_at": "2026-02-16T12:00:00Z",
                "updated_at": "2026-02-16T12:00:00Z"
            }
            mock_post_bob.return_value = mock_response

            result_bob = executor_bob.execute_tool("create_task", {
                "title": "Bob's Task"
            })

            # Verify Bob's request used his user_id
            call_args = mock_post_bob.call_args
            assert "/api/bob/tasks" in call_args[0][0]
            assert result_bob["result"]["user_id"] == "bob"

        executor_bob.close()

    def test_invalid_jwt_returns_authorization_error(self):
        """Test that invalid JWT returns proper error"""
        executor = ToolExecutor(jwt="invalid-jwt", user_id="test-user")

        with patch.object(executor.client, 'post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 403
            mock_response.json.return_value = {"detail": "Invalid or expired token"}
            mock_post.return_value = mock_response

            result = executor.execute_tool("create_task", {
                "title": "Test Task"
            })

            # Verify error is returned with generic message (security)
            assert not result["success"]
            assert result["error_type"] == "authorization"
            # Should not leak "Invalid or expired token" to user
            assert "permission" in result["error"].lower() or "access" in result["error"].lower()

        executor.close()

    def test_cross_user_access_returns_404(self):
        """Test that attempting to access another user's data returns 404"""
        executor = ToolExecutor(jwt="alice-jwt", user_id="alice")

        with patch.object(executor.client, 'post') as mock_post:
            # Backend returns 404 for cross-user access (not 403)
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.json.return_value = {"detail": "Task not found"}
            mock_post.return_value = mock_response

            result = executor.execute_tool("create_task", {
                "title": "Test Task"
            })

            # Verify 404 is handled as authorization error
            assert not result["success"]
            assert result["error_type"] == "authorization"
            # Generic message for security
            assert "couldn't find" in result["error"].lower() or "not found" in result["error"].lower()

        executor.close()

    def test_jwt_not_in_tool_parameters(self):
        """Test that JWT is never passed as a tool parameter"""
        from ai.tools import CreateTaskInput

        # Verify CreateTaskInput schema doesn't have jwt or user_id fields
        schema = CreateTaskInput.model_json_schema()
        properties = schema.get("properties", {})

        assert "jwt" not in properties
        assert "user_id" not in properties
        assert "token" not in properties

        # Only title and description should be present
        assert "title" in properties
        assert "description" in properties

    def test_tool_executor_initialization_requires_jwt(self):
        """Test that ToolExecutor requires JWT and user_id"""
        # Should work with both parameters
        executor = ToolExecutor(jwt="test-jwt", user_id="test-user")
        assert executor.jwt == "test-jwt"
        assert executor.user_id == "test-user"
        executor.close()

        # Should fail without parameters (Python will raise TypeError)
        with pytest.raises(TypeError):
            ToolExecutor()

    def test_jwt_propagated_through_agent_to_executor(self):
        """Test end-to-end JWT propagation from agent to executor"""
        from ai.agent import AIAgent

        with patch('ai.agent.cohere.Client') as mock_cohere:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.text = "Task created"
            mock_response.tool_calls = [
                Mock(name="create_task", parameters={"title": "Test"})
            ]
            mock_client.chat.return_value = mock_response
            mock_cohere.return_value = mock_client

            with patch('ai.agent.ToolExecutor') as mock_executor_class:
                mock_executor_instance = Mock()
                mock_executor_instance.execute_tool.return_value = {
                    "success": True,
                    "result": {
                        "id": 1,
                        "user_id": "test-user",
                        "title": "Test",
                        "description": None,
                        "completed": False,
                        "created_at": "2026-02-16T12:00:00Z",
                        "updated_at": "2026-02-16T12:00:00Z"
                    }
                }
                mock_executor_class.return_value = mock_executor_instance

                with patch.dict(os.environ, {'COHERE_API_KEY': 'test-key'}):
                    agent = AIAgent()
                    agent.process(
                        message="Create a task",
                        conversation_history=[],
                        jwt="test-jwt-token",
                        user_id="test-user"
                    )

                # Verify ToolExecutor was initialized with JWT
                mock_executor_class.assert_called_once()
                call_kwargs = mock_executor_class.call_args[1]
                assert call_kwargs["jwt"] == "test-jwt-token"
                assert call_kwargs["user_id"] == "test-user"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
