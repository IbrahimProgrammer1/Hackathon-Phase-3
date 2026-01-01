"""
Test cases for the Todo Console App.

This module contains test cases for all CLI commands and functionality.
"""

import unittest
from src.models.task import Task
from src.services.task_manager import TaskManager
from src.cli.commands import TodoCLI
from io import StringIO
import sys
from unittest.mock import patch


class TestTask(unittest.TestCase):
    """Test cases for the Task class."""

    def test_task_creation(self):
        """Test creating a task with valid parameters."""
        task = Task(1, "Test title", "Test description")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test title")
        self.assertEqual(task.description, "Test description")
        self.assertEqual(task.status, "incomplete")

    def test_task_creation_with_status(self):
        """Test creating a task with a specific status."""
        task = Task(1, "Test title", "Test description", "complete")
        self.assertEqual(task.status, "complete")

    def test_task_creation_invalid_status(self):
        """Test creating a task with an invalid status."""
        with self.assertRaises(ValueError):
            Task(1, "Test title", "Test description", "invalid")

    def test_task_creation_empty_title(self):
        """Test creating a task with an empty title."""
        with self.assertRaises(ValueError):
            Task(1, "", "Test description")

    def test_task_creation_empty_description(self):
        """Test creating a task with an empty description."""
        with self.assertRaises(ValueError):
            Task(1, "Test title", "")

    def test_task_creation_whitespace_title(self):
        """Test creating a task with whitespace-only title."""
        with self.assertRaises(ValueError):
            Task(1, "   ", "Test description")

    def test_task_update(self):
        """Test updating a task's title and description."""
        task = Task(1, "Original title", "Original description")
        task.update("New title", "New description")
        self.assertEqual(task.title, "New title")
        self.assertEqual(task.description, "New description")

    def test_task_update_partial(self):
        """Test updating only the title or description."""
        task = Task(1, "Original title", "Original description")

        # Update only title
        task.update(new_title="New title")
        self.assertEqual(task.title, "New title")
        self.assertEqual(task.description, "Original description")

        # Update only description
        task.update(new_description="New description")
        self.assertEqual(task.title, "New title")
        self.assertEqual(task.description, "New description")

    def test_task_update_empty_fields(self):
        """Test updating a task with empty fields."""
        task = Task(1, "Original title", "Original description")

        with self.assertRaises(ValueError):
            task.update("", "New description")

        with self.assertRaises(ValueError):
            task.update("New title", "")

    def test_task_toggle_status(self):
        """Test toggling a task's status."""
        task = Task(1, "Test title", "Test description", "incomplete")
        task.toggle_status()
        self.assertEqual(task.status, "complete")

        task.toggle_status()
        self.assertEqual(task.status, "incomplete")

    def test_task_string_representation(self):
        """Test the string representation of a task."""
        task = Task(1, "Test title", "Test description", "incomplete")
        expected = "[1] ⬜ Test title - Test description"
        self.assertEqual(str(task), expected)

        task.status = "complete"
        expected = "[1] ✅ Test title - Test description"
        self.assertEqual(str(task), expected)


class TestTaskManager(unittest.TestCase):
    """Test cases for the TaskManager class."""

    def setUp(self):
        """Set up a TaskManager instance for testing."""
        self.manager = TaskManager()

    def test_add_task(self):
        """Test adding a task."""
        task = self.manager.add_task("Test title", "Test description")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test title")
        self.assertEqual(task.description, "Test description")
        self.assertEqual(len(self.manager.get_all_tasks()), 1)

    def test_get_task_by_id(self):
        """Test getting a task by its ID."""
        task = self.manager.add_task("Test title", "Test description")
        retrieved_task = self.manager.get_task_by_id(task.id)
        self.assertEqual(retrieved_task.id, task.id)
        self.assertIsNone(self.manager.get_task_by_id(999))

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        self.assertEqual(len(self.manager.get_all_tasks()), 0)

        task1 = self.manager.add_task("Title 1", "Description 1")
        task2 = self.manager.add_task("Title 2", "Description 2")

        all_tasks = self.manager.get_all_tasks()
        self.assertEqual(len(all_tasks), 2)
        self.assertEqual(all_tasks[0].id, task1.id)
        self.assertEqual(all_tasks[1].id, task2.id)

    def test_update_task(self):
        """Test updating a task."""
        task = self.manager.add_task("Original title", "Original description")
        updated = self.manager.update_task(task.id, "New title", "New description")

        self.assertTrue(updated)
        updated_task = self.manager.get_task_by_id(task.id)
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "New description")

    def test_update_task_partial(self):
        """Test partially updating a task."""
        task = self.manager.add_task("Original title", "Original description")

        # Update only title
        self.manager.update_task(task.id, new_title="New title")
        updated_task = self.manager.get_task_by_id(task.id)
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "Original description")

        # Update only description
        self.manager.update_task(task.id, new_description="New description")
        updated_task = self.manager.get_task_by_id(task.id)
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "New description")

    def test_update_nonexistent_task(self):
        """Test updating a non-existent task."""
        result = self.manager.update_task(999, "New title", "New description")
        self.assertFalse(result)

    def test_delete_task(self):
        """Test deleting a task."""
        task = self.manager.add_task("Test title", "Test description")
        self.assertEqual(len(self.manager.get_all_tasks()), 1)

        deleted = self.manager.delete_task(task.id)
        self.assertTrue(deleted)
        self.assertEqual(len(self.manager.get_all_tasks()), 0)

    def test_delete_nonexistent_task(self):
        """Test deleting a non-existent task."""
        result = self.manager.delete_task(999)
        self.assertFalse(result)

    def test_toggle_task_status(self):
        """Test toggling a task's status."""
        task = self.manager.add_task("Test title", "Test description")
        self.assertEqual(task.status, "incomplete")

        toggled = self.manager.toggle_task_status(task.id)
        self.assertTrue(toggled)

        updated_task = self.manager.get_task_by_id(task.id)
        self.assertEqual(updated_task.status, "complete")

    def test_toggle_nonexistent_task_status(self):
        """Test toggling status of a non-existent task."""
        result = self.manager.toggle_task_status(999)
        self.assertFalse(result)

    def test_next_id_generation(self):
        """Test that the next ID is correctly generated."""
        self.assertEqual(self.manager.get_next_id(), 1)

        self.manager.add_task("Title 1", "Description 1")
        self.assertEqual(self.manager.get_next_id(), 2)

        self.manager.add_task("Title 2", "Description 2")
        self.assertEqual(self.manager.get_next_id(), 3)


class TestTodoCLI(unittest.TestCase):
    """Test cases for the TodoCLI class."""

    def setUp(self):
        """Set up a TodoCLI instance for testing."""
        self.cli = TodoCLI()

    @patch('builtins.input', side_effect=['quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_quit_command(self, mock_stdout, mock_input):
        """Test the quit command."""
        self.cli.running = True
        self.cli.run()
        self.assertFalse(self.cli.running)

    def test_handle_add_task(self):
        """Test handling the add-task command."""
        args = ["New", "task", "description"]
        self.cli.handle_add_task(args)

        tasks = self.cli.task_manager.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "New")
        self.assertEqual(tasks[0].description, "task description")

    def test_handle_list_tasks_empty(self):
        """Test handling the list-tasks command with no tasks."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.handle_list_tasks()
            output = mock_stdout.getvalue()
            self.assertIn("No tasks found.", output)

    def test_handle_list_tasks_with_tasks(self):
        """Test handling the list-tasks command with tasks."""
        self.cli.task_manager.add_task("Test title", "Test description")

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.handle_list_tasks()
            output = mock_stdout.getvalue()
            self.assertIn("Test title", output)
            self.assertIn("Test description", output)

    def test_handle_update_task(self):
        """Test handling the update-task command."""
        task = self.cli.task_manager.add_task("Original title", "Original description")

        # Test with title only (simulating: update-task 1 "New title")
        args = [str(task.id), "New title"]
        self.cli.handle_update_task(args)

        updated_task = self.cli.task_manager.get_task_by_id(task.id)
        self.assertEqual(updated_task.title, "New title")

        # Reset for next test
        self.cli.task_manager.update_task(task.id, "Original title", "Original description")

        # Test with title and description (simulating: update-task 1 "New title" "New description")
        args = [str(task.id), "New title", "New description"]
        self.cli.handle_update_task(args)

        updated_task = self.cli.task_manager.get_task_by_id(task.id)
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "New description")

    def test_handle_delete_task(self):
        """Test handling the delete-task command."""
        task = self.cli.task_manager.add_task("Test title", "Test description")
        self.assertEqual(len(self.cli.task_manager.get_all_tasks()), 1)

        args = [str(task.id)]
        self.cli.handle_delete_task(args)

        self.assertEqual(len(self.cli.task_manager.get_all_tasks()), 0)

    def test_handle_complete_task(self):
        """Test handling the complete-task command."""
        task = self.cli.task_manager.add_task("Test title", "Test description")
        self.assertEqual(task.status, "incomplete")

        args = [str(task.id)]
        self.cli.handle_complete_task(args)

        updated_task = self.cli.task_manager.get_task_by_id(task.id)
        self.assertEqual(updated_task.status, "complete")


if __name__ == '__main__':
    unittest.main()