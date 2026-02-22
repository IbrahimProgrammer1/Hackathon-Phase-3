"""
Test Suite for AI Tools - Tool Contract Validation

Tests T037: Tool contract test for create_task schema validation
Tests tool schemas, input validation, and output structure.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from pydantic import ValidationError
from ai.tools import (
    ToolRegistry,
    CreateTaskInput,
    CreateTaskOutput,
    ListTasksInput,
    UpdateTaskInput,
    DeleteTaskInput,
    ToggleTaskCompletionInput
)
from datetime import datetime


class TestCreateTaskSchema:
    """T037: Test create_task schema validation"""

    def test_valid_input_with_title_only(self):
        """Test valid input with only title"""
        task_input = CreateTaskInput(title="Buy milk")
        assert task_input.title == "Buy milk"
        assert task_input.description is None

    def test_valid_input_with_title_and_description(self):
        """Test valid input with title and description"""
        task_input = CreateTaskInput(
            title="Buy milk",
            description="Organic whole milk"
        )
        assert task_input.title == "Buy milk"
        assert task_input.description == "Organic whole milk"

    def test_invalid_input_empty_title(self):
        """Test that empty title is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            CreateTaskInput(title="")

        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("title" in str(e.get("loc")) for e in errors)

    def test_invalid_input_missing_title(self):
        """Test that missing title is rejected"""
        with pytest.raises(ValidationError):
            CreateTaskInput()

    def test_invalid_input_title_too_long(self):
        """Test that title exceeding 200 characters is rejected"""
        long_title = "x" * 201
        with pytest.raises(ValidationError) as exc_info:
            CreateTaskInput(title=long_title)

        errors = exc_info.value.errors()
        assert len(errors) > 0

    def test_invalid_input_description_too_long(self):
        """Test that description exceeding 1000 characters is rejected"""
        long_description = "x" * 1001
        with pytest.raises(ValidationError) as exc_info:
            CreateTaskInput(
                title="Valid title",
                description=long_description
            )

        errors = exc_info.value.errors()
        assert len(errors) > 0

    def test_output_schema_structure(self):
        """Test that output schema has correct structure"""
        output = CreateTaskOutput(
            id=1,
            user_id="test-user",
            title="Test Task",
            description="Test Description",
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        assert output.id == 1
        assert output.user_id == "test-user"
        assert output.title == "Test Task"
        assert output.description == "Test Description"
        assert output.completed is False
        assert isinstance(output.created_at, datetime)
        assert isinstance(output.updated_at, datetime)

    def test_tool_registry_validation(self):
        """Test that ToolRegistry validates create_task input correctly"""
        # Valid input
        validated = ToolRegistry.validate_tool_input(
            "create_task",
            {"title": "Buy milk", "description": "Organic"}
        )
        assert validated.title == "Buy milk"
        assert validated.description == "Organic"

        # Invalid input - empty title
        with pytest.raises(ValidationError):
            ToolRegistry.validate_tool_input(
                "create_task",
                {"title": ""}
            )

    def test_tool_registry_get_tool_info(self):
        """Test that create_task tool info is correct"""
        info = ToolRegistry.get_tool_info("create_task")

        assert info["input_schema"] == CreateTaskInput
        assert info["output_schema"] == CreateTaskOutput
        assert info["requires_confirmation"] is False
        assert "create" in info["description"].lower()

    def test_tool_schemas_for_llm_include_create_task(self):
        """Test that create_task is included in LLM tool schemas"""
        # Test Cohere format
        cohere_tools = ToolRegistry.get_tool_schemas_for_llm(provider="cohere")
        create_task_tool = next(
            (t for t in cohere_tools if t["name"] == "create_task"),
            None
        )

        assert create_task_tool is not None
        assert "title" in create_task_tool["parameter_definitions"]
        assert create_task_tool["parameter_definitions"]["title"]["required"] is True
        assert "description" in create_task_tool["parameter_definitions"]
        assert create_task_tool["parameter_definitions"]["description"]["required"] is False

        # Test OpenAI format
        openai_tools = ToolRegistry.get_tool_schemas_for_llm(provider="openai")
        create_task_tool = next(
            (t for t in openai_tools if t["function"]["name"] == "create_task"),
            None
        )

        assert create_task_tool is not None
        assert "title" in create_task_tool["function"]["parameters"]["properties"]
        assert "title" in create_task_tool["function"]["parameters"]["required"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
