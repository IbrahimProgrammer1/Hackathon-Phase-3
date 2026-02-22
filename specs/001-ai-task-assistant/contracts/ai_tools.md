# AI Tool Contracts: Detailed Specifications

**Feature**: 001-ai-task-assistant | **Date**: 2026-02-11 | **Phase**: III

## Overview

This document provides detailed contract specifications for all AI tools. Each tool maps 1:1 to an existing Phase II REST API endpoint and enforces the same security and validation rules.

## Tool Contract Principles

1. **Explicit Typing**: All tools use Pydantic schemas for type safety
2. **No user_id Parameter**: User identity derived from JWT only
3. **1:1 API Mapping**: Each tool maps to exactly one REST endpoint
4. **Identical Behavior**: Tool execution produces same results as direct API calls
5. **Error Consistency**: Tool errors match REST API error responses

---

## Tool 1: create_task

### Purpose
Creates a new task for the authenticated user.

### Input Schema

```python
class CreateTaskInput(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        description="The title of the task"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional detailed description"
    )
```

### Output Schema

```python
class CreateTaskOutput(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
```

### REST API Mapping

**Endpoint**: `POST /api/{user_id}/tasks`

**Request**:
```json
{
  "title": "Buy milk",
  "description": "Organic whole milk"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "alice",
  "title": "Buy milk",
  "description": "Organic whole milk",
  "completed": false,
  "created_at": "2026-02-11T12:00:00Z",
  "updated_at": "2026-02-11T12:00:00Z"
}
```

### Error Conditions

**ValidationError** (400):
- Empty title
- Title exceeds 200 characters
- Description exceeds 1000 characters

**AuthorizationError** (401):
- Invalid JWT
- Expired token

**SystemError** (500):
- Database connection failure

### LLM Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "create_task",
    "description": "Creates a new task for the user. Use this when the user wants to add a new task, reminder, or todo item.",
    "parameters": {
      "type": "object",
      "properties": {
        "title": {
          "type": "string",
          "description": "The title or name of the task",
          "minLength": 1,
          "maxLength": 200
        },
        "description": {
          "type": "string",
          "description": "Optional additional details about the task",
          "maxLength": 1000
        }
      },
      "required": ["title"]
    }
  }
}
```

---

## Tool 2: list_tasks

### Purpose
Lists all tasks for the authenticated user.

### Input Schema

```python
class ListTasksInput(BaseModel):
    pass  # No parameters - user_id derived from JWT
```

### Output Schema

```python
class ListTasksOutput(BaseModel):
    tasks: List[Task]
    total_count: int
```

### REST API Mapping

**Endpoint**: `GET /api/{user_id}/tasks`

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": "alice",
    "title": "Buy milk",
    "description": "Organic whole milk",
    "completed": false,
    "created_at": "2026-02-11T12:00:00Z",
    "updated_at": "2026-02-11T12:00:00Z"
  },
  {
    "id": 2,
    "user_id": "alice",
    "title": "Finish report",
    "description": null,
    "completed": true,
    "created_at": "2026-02-10T10:00:00Z",
    "updated_at": "2026-02-11T11:00:00Z"
  }
]
```

### Error Conditions

**AuthorizationError** (401):
- Invalid JWT
- Expired token

**SystemError** (500):
- Database connection failure

### LLM Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "list_tasks",
    "description": "Lists all tasks for the user. Use this when the user wants to see their tasks, check what they need to do, or when you need to resolve an ambiguous task reference.",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  }
}
```

---

## Tool 3: update_task

### Purpose
Updates a task's title and/or description.

### Input Schema

```python
class UpdateTaskInput(BaseModel):
    task_id: int = Field(gt=0, description="The ID of the task to update")
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

    @validator('title', 'description')
    def at_least_one_field(cls, v, values):
        if not v and not values.get('title') and not values.get('description'):
            raise ValueError("At least one of title or description must be provided")
        return v
```

### Output Schema

```python
class UpdateTaskOutput(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
```

### REST API Mapping

**Endpoint**: `PUT /api/{user_id}/tasks/{task_id}`

**Request**:
```json
{
  "title": "Buy organic milk"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "alice",
  "title": "Buy organic milk",
  "description": "Organic whole milk",
  "completed": false,
  "created_at": "2026-02-11T12:00:00Z",
  "updated_at": "2026-02-11T12:30:00Z"
}
```

### Error Conditions

**ValidationError** (400):
- Invalid task_id (≤ 0)
- Empty title
- Title exceeds 200 characters
- Description exceeds 1000 characters
- Neither title nor description provided

**AuthorizationError** (404):
- Task not found (ownership enforcement)

**SystemError** (500):
- Database connection failure

### LLM Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "update_task",
    "description": "Updates a task's title and/or description. Use this when the user wants to change or modify an existing task.",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "integer",
          "description": "The ID of the task to update",
          "minimum": 1
        },
        "title": {
          "type": "string",
          "description": "New title for the task",
          "minLength": 1,
          "maxLength": 200
        },
        "description": {
          "type": "string",
          "description": "New description for the task",
          "maxLength": 1000
        }
      },
      "required": ["task_id"]
    }
  }
}
```

---

## Tool 4: delete_task

### Purpose
Deletes a task. **Requires explicit user confirmation before execution.**

### Input Schema

```python
class DeleteTaskInput(BaseModel):
    task_id: int = Field(gt=0, description="The ID of the task to delete")
```

### Output Schema

```python
class DeleteTaskOutput(BaseModel):
    success: bool
    message: str
    deleted_task_id: int
```

### REST API Mapping

**Endpoint**: `DELETE /api/{user_id}/tasks/{task_id}`

**Response** (204 No Content) or (200 OK):
```json
{
  "success": true,
  "message": "Task deleted successfully",
  "deleted_task_id": 1
}
```

### Error Conditions

**ValidationError** (400):
- Invalid task_id (≤ 0)

**AuthorizationError** (404):
- Task not found (ownership enforcement)

**SystemError** (500):
- Database connection failure

### Confirmation Requirement

**CRITICAL**: AI must obtain explicit user confirmation before invoking this tool.

**Confirmation Flow**:
1. AI calls `list_tasks()` to get task title
2. AI asks: "Are you sure you want to delete '[Task Title]'? Reply YES to confirm."
3. User responds with "YES" (case-insensitive)
4. AI invokes `delete_task(task_id=X)`

**If user does not confirm**: AI must NOT invoke the tool.

### LLM Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "delete_task",
    "description": "Deletes a task. IMPORTANT: You must obtain explicit user confirmation before calling this function. Ask 'Are you sure you want to delete [task title]? Reply YES to confirm.' and only proceed if the user confirms.",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "integer",
          "description": "The ID of the task to delete",
          "minimum": 1
        }
      },
      "required": ["task_id"]
    }
  }
}
```

---

## Tool 5: toggle_task_completion

### Purpose
Toggles a task's completion status.

### Input Schema

```python
class ToggleTaskCompletionInput(BaseModel):
    task_id: int = Field(gt=0, description="The ID of the task")
    completed: bool = Field(description="New completion status")
```

### Output Schema

```python
class ToggleTaskCompletionOutput(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
```

### REST API Mapping

**Endpoint**: `PATCH /api/{user_id}/tasks/{task_id}/complete`

**Request**:
```json
{
  "completed": true
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "alice",
  "title": "Buy milk",
  "description": "Organic whole milk",
  "completed": true,
  "created_at": "2026-02-11T12:00:00Z",
  "updated_at": "2026-02-11T13:00:00Z"
}
```

### Error Conditions

**ValidationError** (400):
- Invalid task_id (≤ 0)

**AuthorizationError** (404):
- Task not found (ownership enforcement)

**SystemError** (500):
- Database connection failure

### LLM Function Definition

```json
{
  "type": "function",
  "function": {
    "name": "toggle_task_completion",
    "description": "Marks a task as complete or incomplete. Use this when the user wants to mark a task as done, complete, finished, or when they want to mark it as incomplete again.",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "integer",
          "description": "The ID of the task",
          "minimum": 1
        },
        "completed": {
          "type": "boolean",
          "description": "true to mark as complete, false to mark as incomplete"
        }
      },
      "required": ["task_id", "completed"]
    }
  }
}
```

---

## Tool Execution Flow

### Standard Flow

```
1. LLM returns tool call with parameters
2. Validate parameters against Pydantic schema
3. Extract JWT from request context
4. Execute tool by calling backend API with JWT
5. Handle response or error
6. Return structured result to LLM
7. LLM formats conversational response
```

### Error Handling Flow

```
1. Tool execution fails
2. Determine error type (validation/authorization/system)
3. Format error for conversation:
   - Validation: Specific, helpful message
   - Authorization: Generic "Task not found"
   - System: Generic "Having trouble" message
4. Return error to LLM
5. LLM presents error conversationally
```

---

## Contract Validation

✅ All tools explicitly typed with Pydantic
✅ All tools map 1:1 to REST API endpoints
✅ No tool accepts user_id as parameter
✅ All error conditions documented
✅ Confirmation requirement specified for delete_task
✅ LLM function definitions provided
✅ Ready for implementation
