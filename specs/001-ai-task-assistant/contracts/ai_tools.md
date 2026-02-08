# AI Tool Contracts

The following tools are exposed to the AI assistant. Each tool execution requires a valid JWT for the authenticated user.

## create_task
Creates a new task for the authenticated user.
- **Arguments**:
    - `title` (string, required): The title of the task.
    - `description` (string, optional): Detailed description.
- **Backend Service**: `TaskService.create_task(user_id, title, description)`

## list_tasks
Lists tasks for the authenticated user.
- **Arguments**:
    - `completed` (boolean, optional): Filter by completion status.
- **Backend Service**: `TaskService.get_user_tasks(user_id, completed)`

## update_task
Updates an existing task.
- **Arguments**:
    - `task_id` (integer, required): The ID of the task.
    - `title` (string, optional): New title.
    - `description` (string, optional): New description.
- **Backend Service**: `TaskService.update_task(user_id, task_id, title, description)`

## delete_task
Deletes a task. **Requires user confirmation.**
- **Arguments**:
    - `task_id` (integer, required): The ID of the task to delete.
- **Backend Service**: `TaskService.delete_task(user_id, task_id)`

## toggle_task_completion
Toggles the completion status of a task.
- **Arguments**:
    - `task_id` (integer, required): The ID of the task.
    - `completed` (boolean, required): The target completion status.
- **Backend Service**: `TaskService.toggle_task(user_id, task_id, completed)`
