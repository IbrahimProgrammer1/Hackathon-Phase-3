"""
Task model for the Todo Console App.

This module defines the Task class which represents a todo item
with id, title, description, and status attributes.
"""

from typing import Union


class Task:
    """
    Represents a todo item with id, title, description, and status attributes.

    Attributes:
        id (int): auto-generated integer, unique identifier
        title (str): non-empty task title
        description (str): non-empty task description
        status (str): values are "incomplete" or "complete"
    """

    def __init__(self, task_id: int, title: str, description: str, status: str = "incomplete"):
        """
        Initialize a Task instance.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Task title (non-empty)
            description (str): Task description (non-empty)
            status (str): Task status, either "incomplete" or "complete" (default: "incomplete")

        Raises:
            ValueError: If title or description are empty after trimming
        """
        self.id = task_id
        self.title = self._validate_non_empty(title, "title")
        self.description = self._validate_non_empty(description, "description")

        if status not in ["incomplete", "complete"]:
            raise ValueError(f"Status must be 'incomplete' or 'complete', got '{status}'")
        self.status = status

    def _validate_non_empty(self, value: str, field_name: str) -> str:
        """
        Validate that a string value is not empty after trimming.

        Args:
            value (str): The string value to validate
            field_name (str): The name of the field for error messages

        Returns:
            str: The trimmed value

        Raises:
            ValueError: If the value is empty after trimming
        """
        trimmed_value = value.strip()
        if not trimmed_value:
            raise ValueError(f"{field_name.capitalize()} cannot be empty")
        return trimmed_value

    def update(self, new_title: Union[str, None] = None, new_description: Union[str, None] = None) -> None:
        """
        Update the task's title and/or description.

        Args:
            new_title (str, optional): New title for the task
            new_description (str, optional): New description for the task
        """
        if new_title is not None:
            self.title = self._validate_non_empty(new_title, "title")
        if new_description is not None:
            self.description = self._validate_non_empty(new_description, "description")

    def toggle_status(self) -> None:
        """Toggle the task's status between 'complete' and 'incomplete'."""
        if self.status == "complete":
            self.status = "incomplete"
        else:
            self.status = "complete"

    def __str__(self) -> str:
        """
        Return a string representation of the task.

        Returns:
            str: Formatted string representation of the task
        """
        # Using [X] and [ ] instead of emojis to avoid encoding issues on Windows
        status_indicator = "[X]" if self.status == "complete" else "[ ]"
        return f"[{self.id}] {status_indicator} {self.title} - {self.description}"

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the task.

        Returns:
            str: Detailed string representation of the task
        """
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', status='{self.status}')"