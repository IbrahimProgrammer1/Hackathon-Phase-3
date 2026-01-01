"""
CLI commands for the Todo Console App.

This module provides all the command-line interface functionality for the todo app.
"""

import sys
import os
import importlib.util
from typing import Optional, List

# Add the src directory to the path so imports work correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(current_dir))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from src.services.task_manager import TaskManager


class TodoCLI:
    """
    Command-line interface for the Todo Console App.
    """

    def __init__(self):
        """Initialize the TodoCLI with a TaskManager instance."""
        self.task_manager = TaskManager()
        self.running = True

    def run(self) -> None:
        """Run the main CLI loop."""
        print("Welcome to the Todo Console App!")
        print("Available commands: add-task, list-tasks, update-task, delete-task, complete-task, quit")
        print("Type 'help' for more information or 'quit' to exit.\n")

        while self.running:
            try:
                # Read command from user input
                user_input = input("todo> ").strip()

                if not user_input:
                    continue

                # Split the input into command and arguments
                parts = user_input.split()
                command = parts[0].lower()

                # Handle the command
                if command == "quit" or command == "exit":
                    self.handle_quit()
                elif command == "add-task":
                    self.handle_add_task(parts[1:])
                elif command == "list-tasks":
                    self.handle_list_tasks()
                elif command == "update-task":
                    self.handle_update_task(parts[1:])
                elif command == "delete-task":
                    self.handle_delete_task(parts[1:])
                elif command == "complete-task":
                    self.handle_complete_task(parts[1:])
                elif command == "help":
                    self.handle_help()
                else:
                    print(f"Error: Unknown command '{command}'. Use: add-task, list-tasks, update-task, delete-task, complete-task, quit")
            except KeyboardInterrupt:
                print("\nExiting todo app. Goodbye!")
                break
            except EOFError:
                print("\nExiting todo app. Goodbye!")
                break

    def handle_add_task(self, args: List[str]) -> None:
        """
        Handle the add-task command.

        Args:
            args: List of arguments for the command
        """
        if len(args) < 2:
            print("Error: add-task requires a title and description")
            return

        title = args[0]
        description = " ".join(args[1:])

        # Handle quoted titles/descriptions
        if args[0].startswith('"') and len(args) > 1:
            # Find where the title ends
            title_parts = []
            for i, arg in enumerate(args):
                title_parts.append(arg)
                if arg.endswith('"') and not arg.endswith('\\"'):
                    # End of quoted title found
                    title = " ".join(title_parts)[1:-1]  # Remove quotes
                    description = " ".join(args[i+1:])
                    break
            else:
                # No closing quote found, treat first arg as title
                title = args[0]
                description = " ".join(args[1:])

        try:
            task = self.task_manager.add_task(title, description)
            print(f"Task {task.id} added successfully")
        except ValueError as e:
            print(f"Error: {str(e)}")

    def handle_list_tasks(self) -> None:
        """Handle the list-tasks command."""
        tasks = self.task_manager.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            print(task)

    def handle_update_task(self, args: List[str]) -> None:
        """
        Handle the update-task command with support for partial updates.

        Args:
            args: List of arguments for the command
        """
        if len(args) < 2:
            print("Error: update-task requires an ID and at least one field to update")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print(f"Error: Invalid task ID '{args[0]}'. Please provide a numeric ID.")
            return

        # Handle quoted titles/descriptions
        new_title = None
        new_description = None

        # Check if the input contains quoted strings
        original_input = " ".join(args[1:])

        # Check if we have quoted strings
        if '"' in original_input:
            # Parse the input considering quotes
            parts = []
            current_part = []
            in_quotes = False
            i = 0
            while i < len(original_input):
                char = original_input[i]
                if char == '"':
                    in_quotes = not in_quotes
                    i += 1
                elif char == ' ' and not in_quotes:
                    if current_part:
                        parts.append("".join(current_part))
                        current_part = []
                    i += 1
                else:
                    current_part.append(char)
                    i += 1

            # Add the last part if exists
            if current_part:
                parts.append("".join(current_part))

            # Now parts contains properly parsed quoted strings
            if len(parts) >= 1:
                new_title = parts[0]
            if len(parts) >= 2:
                new_description = parts[1]
        else:
            # No quotes, for the case where we want to allow multi-word titles/descriptions without quotes
            # We'll implement a simple approach where if there are 3+ args, the 2nd is title and the rest is description
            if len(args) == 2:  # Only title provided
                new_title = args[1]
            elif len(args) == 3:  # Title and description provided
                new_title = args[1]
                new_description = args[2]
            else:  # More than 3 args - combine remaining args for description
                new_title = args[1]
                new_description = " ".join(args[2:])

        # Validate that at least one field is provided
        if new_title is None and new_description is None:
            print("Error: update-task requires at least a new title or new description")
            return

        # Check if either field is empty after trimming (but allow empty strings for partial updates)
        if new_title is not None and new_title.strip() == "":
            new_title = None  # Treat empty string as no update
        if new_description is not None and new_description.strip() == "":
            new_description = None  # Treat empty string as no update

        # If both are None after handling empty strings, it's an error
        if new_title is None and new_description is None:
            print("Error: update-task requires at least a new title or new description")
            return

        updated = self.task_manager.update_task(task_id, new_title, new_description)
        if updated:
            print(f"Task {task_id} updated successfully")
        else:
            print(f"Error: Task with ID {task_id} does not exist")

    def handle_delete_task(self, args: List[str]) -> None:
        """
        Handle the delete-task command.

        Args:
            args: List of arguments for the command
        """
        if len(args) != 1:
            print("Error: delete-task requires an ID")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print(f"Error: Invalid task ID '{args[0]}'. Please provide a numeric ID.")
            return

        deleted = self.task_manager.delete_task(task_id)
        if deleted:
            print(f"Task {task_id} has been deleted")
        else:
            print(f"Error: Task with ID {task_id} does not exist")

    def handle_complete_task(self, args: List[str]) -> None:
        """
        Handle the complete-task command which toggles task status.

        Args:
            args: List of arguments for the command
        """
        if len(args) != 1:
            print("Error: complete-task requires an ID")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print(f"Error: Invalid task ID '{args[0]}'. Please provide a numeric ID.")
            return

        toggled = self.task_manager.toggle_task_status(task_id)
        if toggled:
            task = self.task_manager.get_task_by_id(task_id)
            if task and task.status == "complete":
                print(f"Task {task_id} marked as complete")
            else:
                print(f"Task {task_id} marked as incomplete")
        else:
            print(f"Error: Task with ID {task_id} does not exist")

    def handle_quit(self) -> None:
        """Handle the quit command."""
        self.running = False
        print("Exiting todo app. Goodbye!")

    def handle_help(self) -> None:
        """Handle the help command."""
        print("\nTodo Console App Commands:")
        print("  add-task <title> <description>    - Add a new task")
        print("  list-tasks                        - List all tasks")
        print("  update-task <id> [title] [desc]   - Update a task (partial updates allowed)")
        print("  delete-task <id>                  - Delete a task")
        print("  complete-task <id>                - Toggle task completion status")
        print("  quit/exit                         - Exit the application")
        print("  help                              - Show this help message")
        print("\nExamples:")
        print('  add-task "Buy groceries" "Milk, bread, eggs"')
        print("  update-task 1 \"Updated title\"")
        print("  complete-task 1")
        print("")