"""
Tool Schema Definitions for AI-Powered Task Assistant

This module defines Pydantic schemas for all AI tools and provides
a registry for converting them to LLM-compatible function calling format.

All tools enforce the constitutional requirement that user_id is NEVER
accepted as a parameter - it must be derived from JWT claims only.
"""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, validator
from datetime import datetime


# ============================================================================
# INPUT SCHEMAS
# ============================================================================

class CreateTaskInput(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(
        min_length=1,
        max_length=200,
        description="The title of the task"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional detailed description of the task"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread"
            }
        }


class ListTasksInput(BaseModel):
    """Schema for listing tasks. No parameters - user_id derived from JWT."""
    pass


class UpdateTaskInput(BaseModel):
    """Schema for updating a task's title and/or description."""
    task_id: int = Field(
        gt=0,
        description="The ID of the task to update"
    )
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="New title for the task"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="New description for the task"
    )

    @validator('title', 'description')
    def at_least_one_field(cls, v, values):
        """Ensure at least one field is provided for update."""
        if not v and not values.get('title') and not values.get('description'):
            raise ValueError("At least one of title or description must be provided")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": 1,
                "title": "Buy organic groceries"
            }
        }


class DeleteTaskInput(BaseModel):
    """Schema for deleting a task. Requires prior confirmation in conversation."""
    task_id: int = Field(
        gt=0,
        description="The ID of the task to delete"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": 1
            }
        }


class ToggleTaskCompletionInput(BaseModel):
    """Schema for toggling a task's completion status."""
    task_id: int = Field(
        gt=0,
        description="The ID of the task"
    )
    completed: bool = Field(
        description="New completion status (true = completed, false = incomplete)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": 1,
                "completed": True
            }
        }


# ============================================================================
# OUTPUT SCHEMAS
# ============================================================================

class TaskOutput(BaseModel):
    """Base schema for task output."""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime


class CreateTaskOutput(TaskOutput):
    """Output schema for create_task."""
    pass


class ListTasksOutput(BaseModel):
    """Output schema for list_tasks."""
    tasks: List[TaskOutput]
    total_count: int


class UpdateTaskOutput(TaskOutput):
    """Output schema for update_task."""
    pass


class DeleteTaskOutput(BaseModel):
    """Output schema for delete_task."""
    success: bool
    message: str
    deleted_task_id: int


class ToggleTaskCompletionOutput(TaskOutput):
    """Output schema for toggle_task_completion."""
    pass


# ============================================================================
# TOOL REGISTRY
# ============================================================================

class ToolRegistry:
    """
    Central registry of all available tools.

    Provides methods to:
    - Get tool schemas in Cohere's tool calling format
    - Validate tool inputs against schemas
    - Map tool names to their input/output schemas
    """

    TOOLS = {
        "create_task": {
            "input_schema": CreateTaskInput,
            "output_schema": CreateTaskOutput,
            "description": "Creates a new task for the user. Use this when the user wants to add a new task, reminder, or todo item.",
            "requires_confirmation": False
        },
        "list_tasks": {
            "input_schema": ListTasksInput,
            "output_schema": ListTasksOutput,
            "description": "Lists all tasks for the user. Use this when the user wants to see their tasks, check what they need to do, or when you need to resolve an ambiguous task reference.",
            "requires_confirmation": False
        },
        "update_task": {
            "input_schema": UpdateTaskInput,
            "output_schema": UpdateTaskOutput,
            "description": "Updates a task's title and/or description. Use this when the user wants to change or modify an existing task.",
            "requires_confirmation": False
        },
        "delete_task": {
            "input_schema": DeleteTaskInput,
            "output_schema": DeleteTaskOutput,
            "description": "Deletes a task. IMPORTANT: You must obtain explicit user confirmation before calling this function. Ask 'Are you sure you want to delete [task title]? Reply YES to confirm.' and only proceed if the user confirms.",
            "requires_confirmation": True
        },
        "toggle_task_completion": {
            "input_schema": ToggleTaskCompletionInput,
            "output_schema": ToggleTaskCompletionOutput,
            "description": "Marks a task as complete or incomplete. Use this when the user wants to mark a task as done, complete, finished, or when they want to mark it as incomplete again.",
            "requires_confirmation": False
        }
    }

    @classmethod
    def get_tool_schemas_for_llm(cls, provider: str = "cohere") -> List[Dict[str, Any]]:
        """
        Convert tool schemas to LLM function calling format.

        Supports multiple providers:
        - Cohere: Uses parameter_definitions format
        - OpenAI: Uses parameters with JSON schema format

        Args:
            provider: LLM provider name ("cohere" or "openai")

        Returns:
            List of tool definitions in provider-specific format
        """
        if provider.lower() == "openai":
            return cls._get_openai_format()
        else:
            return cls._get_cohere_format()

    @classmethod
    def _get_cohere_format(cls) -> List[Dict[str, Any]]:
        """
        Convert tool schemas to Cohere's tool calling format.

        Cohere expects tools in this format:
        {
            "name": "tool_name",
            "description": "what the tool does",
            "parameter_definitions": {
                "param_name": {
                    "description": "param description",
                    "type": "string|number|boolean|object",
                    "required": true|false
                }
            }
        }
        """
        cohere_tools = []

        for name, tool in cls.TOOLS.items():
            schema = tool["input_schema"].model_json_schema()

            # Convert Pydantic schema to Cohere format
            parameter_definitions = {}
            required_fields = schema.get("required", [])

            for prop_name, prop_schema in schema.get("properties", {}).items():
                param_def = {
                    "description": prop_schema.get("description", ""),
                    "type": cls._convert_type_to_cohere(prop_schema),
                    "required": prop_name in required_fields
                }
                parameter_definitions[prop_name] = param_def

            cohere_tool = {
                "name": name,
                "description": tool["description"],
                "parameter_definitions": parameter_definitions
            }

            cohere_tools.append(cohere_tool)

        return cohere_tools

    @classmethod
    def _get_openai_format(cls) -> List[Dict[str, Any]]:
        """
        Convert tool schemas to OpenAI's function calling format.

        OpenAI expects tools in this format:
        {
            "type": "function",
            "function": {
                "name": "tool_name",
                "description": "what the tool does",
                "parameters": {
                    "type": "object",
                    "properties": {...},
                    "required": [...]
                }
            }
        }
        """
        openai_tools = []

        for name, tool in cls.TOOLS.items():
            schema = tool["input_schema"].model_json_schema()

            openai_tool = {
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool["description"],
                    "parameters": {
                        "type": "object",
                        "properties": schema.get("properties", {}),
                        "required": schema.get("required", [])
                    }
                }
            }

            openai_tools.append(openai_tool)

        return openai_tools

    @classmethod
    def _convert_type_to_cohere(cls, prop_schema: Dict[str, Any]) -> str:
        """Convert JSON schema type to Cohere type."""
        json_type = prop_schema.get("type", "string")

        # Map JSON schema types to Cohere types
        type_mapping = {
            "string": "string",
            "integer": "number",
            "number": "number",
            "boolean": "boolean",
            "object": "object",
            "array": "array"
        }

        return type_mapping.get(json_type, "string")

    @classmethod
    def validate_tool_input(cls, tool_name: str, parameters: Dict[str, Any]) -> BaseModel:
        """
        Validate tool input parameters against the tool's schema.

        Args:
            tool_name: Name of the tool
            parameters: Dictionary of parameters to validate

        Returns:
            Validated Pydantic model instance

        Raises:
            ValueError: If tool not found
            ValidationError: If parameters don't match schema
        """
        if tool_name not in cls.TOOLS:
            raise ValueError(f"Unknown tool: {tool_name}")

        input_schema = cls.TOOLS[tool_name]["input_schema"]

        # Validate and return the model instance
        return input_schema(**parameters)

    @classmethod
    def get_tool_info(cls, tool_name: str) -> Dict[str, Any]:
        """Get tool information including schemas and metadata."""
        if tool_name not in cls.TOOLS:
            raise ValueError(f"Unknown tool: {tool_name}")

        return cls.TOOLS[tool_name]

    @classmethod
    def requires_confirmation(cls, tool_name: str) -> bool:
        """Check if a tool requires user confirmation before execution."""
        if tool_name not in cls.TOOLS:
            return False

        return cls.TOOLS[tool_name]["requires_confirmation"]

    @classmethod
    def list_tool_names(cls) -> List[str]:
        """Get list of all available tool names."""
        return list(cls.TOOLS.keys())
