# Data Model & Tool Schemas: AI-Powered Conversational Task Assistant

**Feature**: 001-ai-task-assistant | **Date**: 2026-02-11 | **Phase**: III

## Overview

This document defines the data structures, tool schemas, and conversation patterns for the Phase III AI-powered conversational assistant. All schemas are explicitly typed using Pydantic for validation and align with existing Phase II REST API structures.

## 1. Core Data Structures

### Task Entity (Existing - Phase II)

```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Note**: No changes to existing Task model. AI layer uses this structure via REST API.

### Conversation Message

```python
class ConversationMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_calls: Optional[List[ToolCall]] = None
    tool_results: Optional[List[ToolResult]] = None
```

### Tool Call

```python
class ToolCall(BaseModel):
    id: str  # Unique identifier for this tool call
    name: str  # Tool name (e.g., "create_task")
    arguments: Dict[str, Any]  # Tool-specific parameters
```

### Tool Result

```python
class ToolResult(BaseModel):
    tool_call_id: str  # References ToolCall.id
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
```

---

## 2. Tool Schemas

All tools are defined using Pydantic models for type safety and validation. Each tool maps 1:1 to an existing Phase II REST API endpoint.

### Tool 1: create_task

**Purpose**: Creates a new task for the authenticated user

**Input Schema**:
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
        description="Optional detailed description of the task"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread"
            }
        }
```

**Output Schema**:
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

**Maps to**: `POST /api/{user_id}/tasks`

**Error Conditions**:
- `ValidationError`: Empty title, title too long, description too long
- `AuthorizationError`: Invalid JWT, expired token
- `SystemError`: Database connection failure

---

### Tool 2: list_tasks

**Purpose**: Lists all tasks for the authenticated user

**Input Schema**:
```python
class ListTasksInput(BaseModel):
    # No parameters - lists all tasks for authenticated user
    # user_id is derived from JWT, not accepted as parameter
    pass
```

**Output Schema**:
```python
class ListTasksOutput(BaseModel):
    tasks: List[Task]
    total_count: int
```

**Maps to**: `GET /api/{user_id}/tasks`

**Error Conditions**:
- `AuthorizationError`: Invalid JWT, expired token
- `SystemError`: Database connection failure

---

### Tool 3: update_task

**Purpose**: Updates task title and/or description

**Input Schema**:
```python
class UpdateTaskInput(BaseModel):
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
```

**Output Schema**:
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

**Maps to**: `PUT /api/{user_id}/tasks/{task_id}`

**Error Conditions**:
- `ValidationError`: Invalid task_id, empty title, fields too long
- `AuthorizationError`: Task not found (404 - ownership enforcement)
- `SystemError`: Database connection failure

---

### Tool 4: delete_task

**Purpose**: Deletes a task (requires prior confirmation in conversation)

**Input Schema**:
```python
class DeleteTaskInput(BaseModel):
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
```

**Output Schema**:
```python
class DeleteTaskOutput(BaseModel):
    success: bool
    message: str
    deleted_task_id: int
```

**Maps to**: `DELETE /api/{user_id}/tasks/{task_id}`

**Error Conditions**:
- `ValidationError`: Invalid task_id
- `AuthorizationError`: Task not found (404 - ownership enforcement)
- `SystemError`: Database connection failure

**Special Handling**: AI must obtain explicit user confirmation before invoking this tool. Confirmation must include task title.

---

### Tool 5: toggle_task_completion

**Purpose**: Toggles task completion status

**Input Schema**:
```python
class ToggleTaskCompletionInput(BaseModel):
    task_id: int = Field(
        gt=0,
        description="The ID of the task to toggle"
    )
    completed: bool = Field(
        description="New completion status (true = completed, false = incomplete)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": 1,
                "completed": true
            }
        }
```

**Output Schema**:
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

**Maps to**: `PATCH /api/{user_id}/tasks/{task_id}/complete`

**Error Conditions**:
- `ValidationError`: Invalid task_id
- `AuthorizationError`: Task not found (404 - ownership enforcement)
- `SystemError`: Database connection failure

---

## 3. Tool Registry

```python
class ToolRegistry:
    """Central registry of all available tools"""

    TOOLS = {
        "create_task": {
            "input_schema": CreateTaskInput,
            "output_schema": CreateTaskOutput,
            "description": "Creates a new task for the user",
            "requires_confirmation": False
        },
        "list_tasks": {
            "input_schema": ListTasksInput,
            "output_schema": ListTasksOutput,
            "description": "Lists all tasks for the user",
            "requires_confirmation": False
        },
        "update_task": {
            "input_schema": UpdateTaskInput,
            "output_schema": UpdateTaskOutput,
            "description": "Updates a task's title and/or description",
            "requires_confirmation": False
        },
        "delete_task": {
            "input_schema": DeleteTaskInput,
            "output_schema": DeleteTaskOutput,
            "description": "Deletes a task (requires confirmation)",
            "requires_confirmation": True
        },
        "toggle_task_completion": {
            "input_schema": ToggleTaskCompletionInput,
            "output_schema": ToggleTaskCompletionOutput,
            "description": "Toggles a task's completion status",
            "requires_confirmation": False
        }
    }

    @classmethod
    def get_tool_schemas_for_llm(cls) -> List[Dict]:
        """Convert tool schemas to LLM function calling format"""
        return [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool["description"],
                    "parameters": tool["input_schema"].model_json_schema()
                }
            }
            for name, tool in cls.TOOLS.items()
        ]
```

---

## 4. Conversation Patterns

### Pattern 1: Simple Task Creation

```
User: "Remind me to buy milk"
  ↓
AI: [Calls create_task(title="Buy milk")]
  ↓
Backend: Returns Task object
  ↓
AI: "I've created a task: 'Buy milk'"
```

### Pattern 2: Ambiguous Reference Resolution

```
User: "Delete the milk task"
  ↓
AI: [Calls list_tasks()]
  ↓
Backend: Returns [Task(id=1, title="Buy milk"), Task(id=2, title="Buy organic milk")]
  ↓
AI: "I found two tasks with 'milk':
     1. Buy milk (ID: 1)
     2. Buy organic milk (ID: 2)
     Which one would you like to delete?"
  ↓
User: "The first one"
  ↓
AI: "Are you sure you want to delete 'Buy milk'? Reply YES to confirm."
  ↓
User: "YES"
  ↓
AI: [Calls delete_task(task_id=1)]
  ↓
Backend: Returns success
  ↓
AI: "I've deleted the task 'Buy milk'"
```

### Pattern 3: Confirmation Required

```
User: "Delete task 5"
  ↓
AI: [Calls list_tasks() to get task title]
  ↓
Backend: Returns Task(id=5, title="Finish report")
  ↓
AI: "Are you sure you want to delete 'Finish report'? Reply YES to confirm."
  ↓
User: "No, wait"
  ↓
AI: "Okay, I won't delete that task."
```

### Pattern 4: Validation Error

```
User: "Create a task"
  ↓
AI: "What would you like the task to be called?"
  ↓
User: ""
  ↓
AI: [Attempts create_task(title="")]
  ↓
Backend: Returns ValidationError
  ↓
AI: "Task title cannot be empty. Please provide a title for your task."
```

### Pattern 5: Authorization Error

```
User: "Show me task 999" (task doesn't exist or belongs to another user)
  ↓
AI: [Calls list_tasks(), filters by ID]
  ↓
Backend: Returns empty list or 404
  ↓
AI: "I couldn't find that task. It may not exist or you may not have access to it."
```

---

## 5. Conversation State Management

### Frontend State

```typescript
interface ChatState {
  messages: ConversationMessage[];  // Last 10 messages
  isLoading: boolean;
  error: string | null;
  pendingConfirmation: {
    action: 'delete';
    taskId: number;
    taskTitle: string;
  } | null;
}
```

### Backend Request

```python
class ChatRequest(BaseModel):
    message: str  # User's current message
    conversation_history: List[ConversationMessage]  # Last 10 messages
    # JWT token in Authorization header (not in body)
```

### Backend Response

```python
class ChatResponse(BaseModel):
    message: str  # AI's response
    tool_calls: Optional[List[ToolCall]] = None
    requires_confirmation: bool = False
    confirmation_details: Optional[Dict] = None
```

---

## 6. Error Response Format

```python
class ErrorResponse(BaseModel):
    error_type: Literal["validation", "authorization", "system"]
    message: str  # User-friendly message
    conversational: bool = True
    details: Optional[Dict] = None  # Internal details (not shown to user)
```

**Examples**:

```python
# Validation Error
ErrorResponse(
    error_type="validation",
    message="Task title cannot be empty. Please provide a title for your task.",
    conversational=True
)

# Authorization Error
ErrorResponse(
    error_type="authorization",
    message="Task not found.",
    conversational=True
)

# System Error
ErrorResponse(
    error_type="system",
    message="I'm having trouble processing your request right now. Please try again in a moment.",
    conversational=True
)
```

---

## 7. Schema Validation Rules

### Input Validation

- All tool inputs validated against Pydantic schemas before execution
- Invalid inputs rejected with clear error messages
- No tool accepts `user_id` as parameter (derived from JWT)

### Output Validation

- All tool outputs match REST API response format
- Structured data returned to LLM for formatting
- LLM converts structured data to conversational response

### Security Validation

- JWT validated before every tool execution
- User identity extracted from JWT claims
- Cross-user access returns 404 (not 403)

---

## Data Model Validation

✅ All tool schemas defined with Pydantic
✅ All schemas map 1:1 to Phase II REST API endpoints
✅ No tool accepts user_id as parameter
✅ All error conditions documented
✅ Conversation patterns cover all user stories
✅ State management aligns with stateless backend requirement
✅ Ready for implementation
