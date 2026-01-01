# Phase I - Todo In-Memory Python Console App

A command-line todo application that stores tasks in memory. The app supports adding, listing, updating, deleting, and marking tasks as complete/incomplete with proper validation and user feedback.

## Features

- Add tasks with title and description
- List all tasks with status indicators (✅ for complete, ⬜ for incomplete)
- Update task details by ID
- Delete tasks by ID
- Mark tasks as complete/incomplete by toggling their status
- In-memory storage (data is lost on exit)
- Input validation and error handling
- Clean, intuitive command-line interface

## Setup

1. Ensure you have Python 3.13+ installed on your system
2. Clone or download this repository
3. Navigate to the project directory

## Usage

Run the application using Python:

```bash
python src/main.py
```

The application will start and display a welcome message. You can then use the following commands:

### Available Commands

- `add-task <title> <description>` - Add a new task
- `list-tasks` - Display all tasks with their ID, status, title, and description
- `update-task <id> [new_title] [new_description]` - Update title and/or description of a task by ID
- `delete-task <id>` - Remove a task by ID
- `complete-task <id>` - Toggle task completion status
- `quit` or `exit` - Exit the application
- `help` - Show help information

### Examples

```bash
# Add a new task
todo> add-task "Buy groceries" "Milk, bread, eggs"

# List all tasks
todo> list-tasks

# Update a task (partial update - only title)
todo> update-task 1 "Updated title only"

# Update a task (partial update - only description)
todo> update-task 1 "" "Updated description only"

# Update a task (both title and description)
todo> update-task 1 "New title" "New description"

# Mark a task as complete/incomplete
todo> complete-task 1

# Delete a task
todo> delete-task 1

# Exit the application
todo> quit
```

### Notes

- Task titles and descriptions cannot be empty
- IDs are auto-generated and unique
- Tasks are displayed in the order they were added
- The application continues running after errors
- All error messages are prefixed with "Error:"

## Project Structure

```
src/
├── main.py              # Main CLI entry point
├── models/
│   └── task.py          # Task class definition
├── services/
│   └── task_manager.py  # Task management logic
├── cli/
│   └── commands.py      # CLI command handlers
└── utils/
    └── validation.py    # Input validation utilities
```

## Development

This project was developed using the Spec-Kit Plus methodology with Claude Code, following a spec-driven development approach:

1. Specification → Define requirements
2. Plan → Architect the solution
3. Tasks → Break down into actionable steps
4. Implement → Execute the build

The implementation follows clean code principles with a clear separation of concerns using models, services, and CLI layers.