# Claude Code Rules - Backend

This file defines the backend-specific rules and conventions for the Phase II Todo Full-Stack Web Application.

## Task context

**Your Surface:** You operate on backend-specific implementation tasks for the Todo application.

**Your Success is Measured By:**
- All API endpoints require JWT authentication
- User ownership is enforced at the API layer
- Database queries are properly filtered by user_id
- API responses follow consistent error formats
- Backend is stateless with JWT-based authentication

## Backend Architecture

### Technology Stack
- FastAPI for the web framework
- SQLModel for ORM and database modeling
- python-jose for JWT handling
- Neon Serverless PostgreSQL for the database
- Uvicorn for the ASGI server

### Project Structure
```
backend/
├── src/
│   ├── models/           # SQLModel database models
│   │   └── task_model.py # Task and User models
│   ├── database/         # Database connection and setup
│   │   └── database.py   # Database engine and session
│   ├── middleware/       # Request processing middleware
│   │   └── auth.py       # JWT verification middleware
│   ├── api/              # API route definitions
│   │   ├── tasks.py      # Task-related endpoints
│   │   └── error_handlers.py # Standardized error responses
│   └── services/         # Business logic (if needed)
├── tests/                # Backend unit and integration tests
├── requirements.txt      # Python dependencies
└── main.py               # Application entry point
```

### API Design
- All endpoints follow the pattern `/api/{user_id}/...`
- JWT token must be provided in Authorization header
- Path user_id must match JWT user_id for all operations
- Error responses follow format: `{ "error": "message", "code": status_code }`

### Authentication & Authorization
- JWT verification middleware on all endpoints
- User identity extracted from JWT (never from client input)
- Ownership enforcement: all queries filtered by authenticated user_id
- Cross-user access attempts return 404 (not found) to avoid leaking information

## Development Guidelines

### 1. Security First
- Never trust user_id from request body or query parameters
- Always verify JWT signature using BETTER_AUTH_SECRET
- Enforce ownership at the database query level
- Implement proper input validation and sanitization

### 2. API Consistency
- Follow RESTful principles for endpoint design
- Use consistent response formats
- Implement proper HTTP status codes (401, 403, 404, etc.)
- Standardize error response format across all endpoints

### 3. Code Quality
- Use Pydantic models for request/response validation
- Implement proper type hints
- Write comprehensive unit tests
- Follow FastAPI best practices

## Backend Responsibilities

### Models
- Task model with user_id foreign key and indexes
- User model managed by Better Auth integration
- Proper validation and constraints

### Endpoints
- `GET /api/{user_id}/tasks` - List user's tasks
- `POST /api/{user_id}/tasks` - Create task for user
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

### Middleware
- JWT verification and token extraction
- User identity validation
- Ownership enforcement

### Error Handling
- Standardized error response format
- Proper HTTP status codes
- Security-conscious error messages

## Testing Strategy

### Backend Tests
- Unit tests for CRUD operations
- Integration tests for authentication
- Authorization tests for ownership enforcement
- API contract tests

## Database Schema

### Tables
- `tasks` table with indexes on `user_id` and `completed` columns
- Foreign key relationship between tasks and users
- Proper constraints and validation

## Deployment

### Environment Variables
- DATABASE_URL - PostgreSQL connection string
- BETTER_AUTH_SECRET - JWT signing secret

### Migrations
- Use Alembic for database migrations
- Properly handle schema changes
- Maintain backward compatibility