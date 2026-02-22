"""
Tool Executor for AI-Powered Task Assistant

This module implements the ToolExecutor class which executes AI tool calls
by directly interacting with the database, avoiding HTTP calls that cause
deadlocks when running within the same server process.

Constitutional Requirements:
- JWT token must be propagated to all operations
- user_id is derived from JWT, never from tool parameters
- Error messages are formatted appropriately for conversation
"""

import os
from typing import Dict, Any, Optional
from pydantic import ValidationError
from sqlmodel import Session, select
from datetime import datetime

from .tools import ToolRegistry
from ..models.task_model import Task
from ..database import engine


class ToolExecutor:
    """
    Executes AI tool calls by directly accessing the database.

    This avoids HTTP deadlock issues when running within the same
    server process that handles the original request.
    """

    def __init__(self, jwt: str, user_id: str, base_url: Optional[str] = None):
        """
        Initialize the ToolExecutor with JWT and user identity.

        Args:
            jwt: JWT token for authentication (not used for direct DB access)
            user_id: User ID extracted from JWT claims
            base_url: Ignored (kept for API compatibility)
        """
        self.jwt = jwt
        self.user_id = user_id

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool by calling the database directly.

        Args:
            tool_name: Name of the tool to execute
            parameters: Tool parameters (already validated by ToolRegistry)

        Returns:
            Dict containing either:
            - success=True, result=<tool output>
            - success=False, error=<error message>, error_type=<type>
        """
        try:
            # Validate tool exists
            if tool_name not in ToolRegistry.TOOLS:
                return self._format_error(
                    "system",
                    f"Unknown tool: {tool_name}",
                    "I'm having trouble processing that request right now."
                )

            # Validate parameters against schema
            try:
                validated_input = ToolRegistry.validate_tool_input(tool_name, parameters)
            except ValidationError as e:
                return self._format_validation_error(e)

            # Execute the appropriate tool
            if tool_name == "create_task":
                return self._execute_create_task(validated_input)
            elif tool_name == "list_tasks":
                return self._execute_list_tasks(validated_input)
            elif tool_name == "update_task":
                return self._execute_update_task(validated_input)
            elif tool_name == "delete_task":
                return self._execute_delete_task(validated_input)
            elif tool_name == "toggle_task_completion":
                return self._execute_toggle_completion(validated_input)
            else:
                return self._format_error(
                    "system",
                    f"Tool not implemented: {tool_name}",
                    "I'm having trouble processing that request right now."
                )

        except Exception as e:
            return self._format_error(
                "system",
                str(e),
                "I'm having trouble processing your request right now. Please try again."
            )

    def _execute_create_task(self, validated_input) -> Dict[str, Any]:
        """Execute create_task tool: Insert into database"""
        try:
            with Session(engine) as session:
                task = Task(
                    user_id=self.user_id,
                    title=validated_input.title,
                    description=validated_input.description,
                    completed=False,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(task)
                session.commit()
                session.refresh(task)

                return {
                    "success": True,
                    "result": {
                        "id": task.id,
                        "user_id": task.user_id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat()
                    }
                }
        except Exception as e:
            return self._format_error("system", str(e),
                "I'm having trouble creating that task right now.")

    def _execute_list_tasks(self, validated_input) -> Dict[str, Any]:
        """Execute list_tasks tool: Query database"""
        try:
            with Session(engine) as session:
                statement = select(Task).where(Task.user_id == self.user_id)
                tasks = session.exec(statement).all()

                return {
                    "success": True,
                    "result": {
                        "tasks": [
                            {
                                "id": task.id,
                                "user_id": task.user_id,
                                "title": task.title,
                                "description": task.description,
                                "completed": task.completed,
                                "created_at": task.created_at.isoformat(),
                                "updated_at": task.updated_at.isoformat()
                            }
                            for task in tasks
                        ],
                        "total_count": len(tasks)
                    }
                }
        except Exception as e:
            return self._format_error("system", str(e),
                "I'm having trouble retrieving your tasks right now.")

    def _execute_update_task(self, validated_input) -> Dict[str, Any]:
        """Execute update_task tool: Update database"""
        try:
            with Session(engine) as session:
                statement = select(Task).where(
                    Task.user_id == self.user_id,
                    Task.id == validated_input.task_id
                )
                task = session.exec(statement).first()

                if not task:
                    return self._format_error(
                        "authorization",
                        "Task not found",
                        "I couldn't find that task."
                    )

                if validated_input.title is not None:
                    task.title = validated_input.title
                if validated_input.description is not None:
                    task.description = validated_input.description
                task.updated_at = datetime.utcnow()

                session.add(task)
                session.commit()
                session.refresh(task)

                return {
                    "success": True,
                    "result": {
                        "id": task.id,
                        "user_id": task.user_id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat()
                    }
                }
        except Exception as e:
            return self._format_error("system", str(e),
                "I'm having trouble updating that task right now.")

    def _execute_delete_task(self, validated_input) -> Dict[str, Any]:
        """Execute delete_task tool: Delete from database"""
        try:
            with Session(engine) as session:
                statement = select(Task).where(
                    Task.user_id == self.user_id,
                    Task.id == validated_input.task_id
                )
                task = session.exec(statement).first()

                if not task:
                    return self._format_error(
                        "authorization",
                        "Task not found",
                        "I couldn't find that task."
                    )

                session.delete(task)
                session.commit()

                return {
                    "success": True,
                    "result": {
                        "success": True,
                        "message": "Task deleted successfully",
                        "deleted_task_id": validated_input.task_id
                    }
                }
        except Exception as e:
            return self._format_error("system", str(e),
                "I'm having trouble deleting that task right now.")

    def _execute_toggle_completion(self, validated_input) -> Dict[str, Any]:
        """Execute toggle_task_completion tool: Update completion status"""
        try:
            with Session(engine) as session:
                statement = select(Task).where(
                    Task.user_id == self.user_id,
                    Task.id == validated_input.task_id
                )
                task = session.exec(statement).first()

                if not task:
                    return self._format_error(
                        "authorization",
                        "Task not found",
                        "I couldn't find that task."
                    )

                task.completed = validated_input.completed
                task.updated_at = datetime.utcnow()

                session.add(task)
                session.commit()
                session.refresh(task)

                return {
                    "success": True,
                    "result": {
                        "id": task.id,
                        "user_id": task.user_id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat()
                    }
                }
        except Exception as e:
            return self._format_error("system", str(e),
                "I'm having trouble updating that task right now.")

    def _handle_error_response(self, response) -> Dict[str, Any]:
        """Handle HTTP error responses (kept for API compatibility)."""
        return self._format_error(
            "system",
            f"HTTP {response.status_code}",
            "I'm having trouble processing your request right now."
        )

    def _format_validation_error(self, error: ValidationError) -> Dict[str, Any]:
        """Format Pydantic validation errors for conversation."""
        errors = error.errors()
        if not errors:
            return self._format_error(
                "validation",
                "Validation failed",
                "There was a problem with the information provided."
            )

        first_error = errors[0]
        field = first_error.get("loc", ["unknown"])[-1]
        msg = first_error.get("msg", "Invalid value")
        conversational_msg = self._make_conversational_validation_error(f"{field}: {msg}")

        return self._format_error("validation", str(error), conversational_msg)

    def _make_conversational_validation_error(self, error_detail: str) -> str:
        """Convert technical error messages to conversational ones."""
        error_lower = error_detail.lower()
        if "title" in error_lower and ("empty" in error_lower or "min_length" in error_lower):
            return "Task title cannot be empty."
        elif "title" in error_lower and "max_length" in error_lower:
            return "Task title is too long. Keep it under 200 characters."
        elif "task_id" in error_lower and ("greater than" in error_lower or "invalid" in error_lower):
            return "Invalid task ID."
        else:
            return f"There was a problem: {error_detail}"

    def _format_error(self, error_type: str, internal_message: str,
                     conversational_message: str) -> Dict[str, Any]:
        """Format an error response."""
        return {
            "success": False,
            "error": conversational_message,
            "error_type": error_type,
            "internal_error": internal_message
        }

    def close(self):
        """No-op for API compatibility."""
        pass
