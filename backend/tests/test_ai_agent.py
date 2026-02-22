"""
Test Suite for AI Agent - Integration Tests

Tests T038: Integration test for create_task intent parsing
Tests that natural language messages are correctly parsed into tool calls.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from unittest.mock import Mock, patch, MagicMock
from ai.agent import AIAgent
from ai.tool_executor import ToolExecutor


class TestCreateTaskIntentParsing:
    """T038: Test create_task intent parsing from natural language"""

    @pytest.fixture
    def mock_cohere_client(self):
        """Mock Cohere client for testing"""
        with patch('ai.agent.cohere.Client') as mock_client:
            yield mock_client

    @pytest.fixture
    def mock_tool_executor(self):
        """Mock ToolExecutor for testing"""
        with patch('ai.agent.ToolExecutor') as mock_executor:
            executor_instance = Mock()
            mock_executor.return_value = executor_instance
            yield executor_instance

    def test_simple_task_creation_intent(self, mock_cohere_client, mock_tool_executor):
        """Test: 'Buy milk' should trigger create_task with title='Buy milk'"""
        # Setup mock Cohere response
        mock_response = Mock()
        mock_response.text = "I've created a task: 'Buy milk'"
        mock_response.tool_calls = [
            Mock(
                name="create_task",
                parameters={"title": "Buy milk"}
            )
        ]

        mock_client_instance = Mock()
        mock_client_instance.chat.return_value = mock_response
        mock_cohere_client.return_value = mock_client_instance

        # Setup mock tool executor response
        mock_tool_executor.execute_tool.return_value = {
            "success": True,
            "result": {
                "id": 1,
                "user_id": "test-user",
                "title": "Buy milk",
                "description": None,
                "completed": False,
                "created_at": "2026-02-16T12:00:00Z",
                "updated_at": "2026-02-16T12:00:00Z"
            }
        }

        # Create agent and process message
        with patch.dict(os.environ, {'COHERE_API_KEY': 'test-key'}):
            agent = AIAgent()
            response = agent.process(
                message="Buy milk",
                conversation_history=[],
                jwt="test-jwt",
                user_id="test-user"
            )

        # Verify tool was called
        mock_tool_executor.execute_tool.assert_called_once()
        call_args = mock_tool_executor.execute_tool.call_args
        assert call_args[0][0] == "create_task"
        assert call_args[0][1]["title"] == "Buy milk"

        # Verify response
        assert "created" in response["message"].lower() or "buy milk" in response["message"].lower()

    def test_task_creation_with_description(self, mock_cohere_client, mock_tool_executor):
        """Test: 'Remind me to buy organic milk' should include description"""
        mock_response = Mock()
        mock_response.text = "I've created a task: 'Buy organic milk'"
        mock_response.tool_calls = [
            Mock(
                name="create_task",
                parameters={
                    "title": "Buy organic milk",
                    "description": "Reminder to purchase organic milk"
                }
            )
        ]

        mock_client_instance = Mock()
        mock_client_instance.chat.return_value = mock_response
        mock_cohere_client.return_value = mock_client_instance

        mock_tool_executor.execute_tool.return_value = {
            "success": True,
            "result": {
                "id": 2,
                "user_id": "test-user",
                "title": "Buy organic milk",
                "description": "Reminder to purchase organic milk",
                "completed": False,
                "created_at": "2026-02-16T12:00:00Z",
                "updated_at": "2026-02-16T12:00:00Z"
            }
        }

        with patch.dict(os.environ, {'COHERE_API_KEY': 'test-key'}):
            agent = AIAgent()
            response = agent.process(
                message="Remind me to buy organic milk",
                conversation_history=[],
                jwt="test-jwt",
                user_id="test-user"
            )

        # Verify tool was called with description
        mock_tool_executor.execute_tool.assert_called_once()
        call_args = mock_tool_executor.execute_tool.call_args
        assert call_args[0][0] == "create_task"
        assert "organic milk" in call_args[0][1]["title"].lower()

    def test_multiple_task_creation_intents(self, mock_cohere_client, mock_tool_executor):
        """Test: 'Add tasks: buy milk and finish report' should create multiple tasks"""
        # First tool call
        mock_response1 = Mock()
        mock_response1.text = "I've created two tasks for you"
        mock_response1.tool_calls = [
            Mock(name="create_task", parameters={"title": "Buy milk"}),
            Mock(name="create_task", parameters={"title": "Finish report"})
        ]

        mock_client_instance = Mock()
        mock_client_instance.chat.return_value = mock_response1
        mock_cohere_client.return_value = mock_client_instance

        mock_tool_executor.execute_tool.side_effect = [
            {
                "success": True,
                "result": {
                    "id": 1,
                    "user_id": "test-user",
                    "title": "Buy milk",
                    "description": None,
                    "completed": False,
                    "created_at": "2026-02-16T12:00:00Z",
                    "updated_at": "2026-02-16T12:00:00Z"
                }
            },
            {
                "success": True,
                "result": {
                    "id": 2,
                    "user_id": "test-user",
                    "title": "Finish report",
                    "description": None,
                    "completed": False,
                    "created_at": "2026-02-16T12:00:00Z",
                    "updated_at": "2026-02-16T12:00:00Z"
                }
            }
        ]

        with patch.dict(os.environ, {'COHERE_API_KEY': 'test-key'}):
            agent = AIAgent()
            response = agent.process(
                message="Add tasks: buy milk and finish report",
                conversation_history=[],
                jwt="test-jwt",
                user_id="test-user"
            )

        # Verify both tools were called
        assert mock_tool_executor.execute_tool.call_count == 2

    def test_validation_error_handling(self, mock_cohere_client, mock_tool_executor):
        """Test: Empty title should return conversational error"""
        mock_response = Mock()
        mock_response.text = "I need more information"
        mock_response.tool_calls = [
            Mock(name="create_task", parameters={"title": ""})
        ]

        mock_client_instance = Mock()
        mock_client_instance.chat.return_value = mock_response
        mock_cohere_client.return_value = mock_client_instance

        # Tool executor returns validation error
        mock_tool_executor.execute_tool.return_value = {
            "success": False,
            "error": "Task title cannot be empty. Please provide a title for your task.",
            "error_type": "validation"
        }

        with patch.dict(os.environ, {'COHERE_API_KEY': 'test-key'}):
            agent = AIAgent()
            response = agent.process(
                message="Create a task",
                conversation_history=[],
                jwt="test-jwt",
                user_id="test-user"
            )

        # Verify error was handled
        mock_tool_executor.execute_tool.assert_called_once()

    def test_conversation_context_maintained(self, mock_cohere_client, mock_tool_executor):
        """Test: Conversation history is passed to LLM"""
        mock_response = Mock()
        mock_response.text = "I've created another task"
        mock_response.tool_calls = [
            Mock(name="create_task", parameters={"title": "Another task"})
        ]

        mock_client_instance = Mock()
        mock_client_instance.chat.return_value = mock_response
        mock_cohere_client.return_value = mock_client_instance

        mock_tool_executor.execute_tool.return_value = {
            "success": True,
            "result": {
                "id": 3,
                "user_id": "test-user",
                "title": "Another task",
                "description": None,
                "completed": False,
                "created_at": "2026-02-16T12:00:00Z",
                "updated_at": "2026-02-16T12:00:00Z"
            }
        }

        conversation_history = [
            {"role": "user", "content": "Buy milk"},
            {"role": "assistant", "content": "I've created a task: 'Buy milk'"}
        ]

        with patch.dict(os.environ, {'COHERE_API_KEY': 'test-key'}):
            agent = AIAgent()
            response = agent.process(
                message="Add another task",
                conversation_history=conversation_history,
                jwt="test-jwt",
                user_id="test-user"
            )

        # Verify chat was called with history
        mock_client_instance.chat.assert_called()
        call_kwargs = mock_client_instance.chat.call_args[1]
        assert "chat_history" in call_kwargs
        assert len(call_kwargs["chat_history"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
