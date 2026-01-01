"""
TaskManager service for the Todo Console App.

This module provides in-memory storage and management of tasks.
"""

import sys
import os
from typing import List, Optional

# Add the src directory to the path so imports work correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from src.models.task import Task


class TaskManager:
    """
    Manages tasks in memory with methods to add, update, delete, and list tasks.
    """

    def __init__(self):
        """Initialize the TaskManager with an empty list of tasks and an ID counter."""
        self.tasks: List[Task] = []
        self._next_id = 1

    def add_task(self, title: str, description: str) -> Task:
        """
        Add a new task with the given title and description.

        Args:
            title (str): The title of the task
            description (str): The description of the task

        Returns:
            Task: The newly created task

        Raises:
            ValueError: If title or description are empty
        """
        task = Task(self._next_id, title, description)
        self.tasks.append(task)
        self._next_id += 1
        return task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task or None: The task with the given ID, or None if not found
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List[Task]: A list of all tasks in insertion order
        """
        return self.tasks.copy()

    def update_task(self, task_id: int, new_title: Optional[str] = None, new_description: Optional[str] = None) -> bool:
        """
        Update a task's title and/or description by ID.

        Args:
            task_id (int): The ID of the task to update
            new_title (str, optional): New title for the task
            new_description (str, optional): New description for the task

        Returns:
            bool: True if the task was updated, False if the task was not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        task.update(new_title, new_description)
        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if the task was not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        self.tasks.remove(task)
        return True

    def toggle_task_status(self, task_id: int) -> bool:
        """
        Toggle a task's status between 'complete' and 'incomplete'.

        Args:
            task_id (int): The ID of the task to toggle

        Returns:
            bool: True if the task status was toggled, False if the task was not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        task.toggle_status()
        return True

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new task.

        Returns:
            int: The next available ID
        """
        return self._next_id