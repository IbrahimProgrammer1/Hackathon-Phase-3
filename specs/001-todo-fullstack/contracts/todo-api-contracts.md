# API Contracts: Phase II Todo Full-Stack Web App

## Base Path
`/api/{user_id}`

## Common Headers
- `Authorization: Bearer <JWT_TOKEN>` (required for all endpoints)
- `Content-Type: application/json` (for POST/PUT/PATCH requests)

## Error Response Format
```json
{
  "error": "Description of failure",
  "code": <HTTP status code>
}
```

## Endpoints

### GET /tasks
**Description**: List all tasks belonging to authenticated user

**Path Parameters**:
- `user_id` (string, required): Must match the authenticated user's ID from JWT

**Response**:
- `200 OK`: Array of task objects
```json
[
  {
    "id": 1,
    "user_id": "user123",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "created_at": "2026-01-06T10:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z"
  }
]
```
- `401 Unauthorized`: Invalid or missing JWT
- `403 Forbidden`: Path user_id doesn't match JWT user_id

### POST /tasks
**Description**: Create a new task for authenticated user

**Path Parameters**:
- `user_id` (string, required): Must match the authenticated user's ID from JWT

**Request Body**:
```json
{
  "title": "Task title",
  "description": "Task description (optional)"
}
```

**Response**:
- `201 Created`: New task object
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "created_at": "2026-01-06T10:00:00Z",
  "updated_at": "2026-01-06T10:00:00Z"
}
```
- `400 Bad Request`: Invalid request body (e.g., missing title)
- `401 Unauthorized`: Invalid or missing JWT
- `403 Forbidden`: Path user_id doesn't match JWT user_id

### GET /tasks/{id}
**Description**: Retrieve a single task owned by authenticated user

**Path Parameters**:
- `user_id` (string, required): Must match the authenticated user's ID from JWT
- `id` (integer, required): Task ID

**Response**:
- `200 OK`: Task object
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "created_at": "2026-01-06T10:00:00Z",
  "updated_at": "2026-01-06T10:00:00Z"
}
```
- `400 Bad Request`: Invalid task ID format
- `401 Unauthorized`: Invalid or missing JWT
- `403 Forbidden`: Path user_id doesn't match JWT user_id
- `404 Not Found`: Task doesn't exist OR belongs to another user (no distinction for security)

### PUT /tasks/{id}
**Description**: Update task title and/or description

**Path Parameters**:
- `user_id` (string, required): Must match the authenticated user's ID from JWT
- `id` (integer, required): Task ID

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description"
}
```

**Response**:
- `200 OK`: Updated task object
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": false,
  "created_at": "2026-01-06T10:00:00Z",
  "updated_at": "2026-01-06T11:00:00Z"
}
```
- `400 Bad Request`: Invalid request body or task ID format
- `401 Unauthorized`: Invalid or missing JWT
- `403 Forbidden`: Path user_id doesn't match JWT user_id
- `404 Not Found`: Task doesn't exist OR belongs to another user (no distinction for security)

### DELETE /tasks/{id}
**Description**: Delete task owned by authenticated user

**Path Parameters**:
- `user_id` (string, required): Must match the authenticated user's ID from JWT
- `id` (integer, required): Task ID

**Response**:
- `204 No Content`: Task successfully deleted
- `400 Bad Request`: Invalid task ID format
- `401 Unauthorized`: Invalid or missing JWT
- `403 Forbidden`: Path user_id doesn't match JWT user_id
- `404 Not Found`: Task doesn't exist OR belongs to another user (no distinction for security)

### PATCH /tasks/{id}/complete
**Description**: Toggle task completion status

**Path Parameters**:
- `user_id` (string, required): Must match the authenticated user's ID from JWT
- `id` (integer, required): Task ID

**Request Body**:
```json
{
  "completed": true
}
```

**Response**:
- `200 OK`: Updated task object with new completion status
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Task title",
  "description": "Task description",
  "completed": true,
  "created_at": "2026-01-06T10:00:00Z",
  "updated_at": "2026-01-06T11:00:00Z"
}
```
- `400 Bad Request`: Invalid request body or task ID format
- `401 Unauthorized`: Invalid or missing JWT
- `403 Forbidden`: Path user_id doesn't match JWT user_id
- `404 Not Found`: Task doesn't exist OR belongs to another user (no distinction for security)