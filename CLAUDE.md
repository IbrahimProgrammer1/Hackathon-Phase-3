# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-phase todo application following Spec-Driven Development (SDD) with Spec-Kit Plus:

- **Phase I** (frozen): Python console app in `src/` - in-memory task management
- **Phase II** (frozen): Full-stack web app with authentication and persistent storage
- **Phase III** (current): AI-powered conversational interface extending Phase II

**Critical**: Previous phase artifacts are immutable. Never modify Phase I or Phase II code unless explicitly requested.

## Development Commands

### Backend (FastAPI)

```bash
# Navigate to backend
cd backend

# Create/activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --port 8000

# Run tests
python -m pytest
python -m pytest backend/tests/test_tasks.py  # Single test file
python -m pytest -v  # Verbose output

# Run specific test
python -m pytest backend/tests/test_tasks.py::test_create_task
```

### Frontend (Next.js)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev  # Starts on http://localhost:3000

# Build for production
npm run build

# Run production build
npm start

# Lint
npm run lint

# Run tests (if configured)
npm run test
```

### Docker Compose

```bash
# Start all services (backend, frontend, PostgreSQL)
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build
```

### Quick Start Scripts

```bash
# Start backend (handles venv creation and dependencies)
./start_backend.sh  # or start_backend.bat on Windows

# Start frontend (handles npm install)
./start_frontend.sh  # or start_frontend.bat on Windows
```

## Architecture

### Monorepo Structure

```
├── backend/              # FastAPI application
│   ├── src/
│   │   ├── api/         # Route handlers (tasks.py, auth.py)
│   │   ├── models/      # SQLModel database models
│   │   ├── middleware/  # JWT authentication (auth.py)
│   │   ├── database/    # Database connection setup
│   │   └── services/    # Business logic layer
│   ├── tests/           # pytest tests
│   ├── main.py          # FastAPI app entry point
│   └── requirements.txt
├── frontend/            # Next.js application
│   ├── src/
│   │   ├── app/        # App Router pages (auth/, tasks/)
│   │   ├── components/ # React components
│   │   ├── lib/        # API client (api.ts), auth (auth.ts)
│   │   ├── contexts/   # React contexts
│   │   └── services/   # Business logic
│   └── package.json
├── src/                 # Phase I console app (FROZEN)
└── specs/               # Feature specifications
```

### Authentication Flow

1. User logs in via Better Auth → receives JWT token
2. Frontend stores token in localStorage (see `frontend/src/lib/authStorage.ts`)
3. All API requests include `Authorization: Bearer <token>` header
4. Backend middleware (`backend/src/middleware/auth.py`) verifies JWT
5. User identity extracted from JWT claims (never from request body)
6. All operations filtered by authenticated `user_id`

**Security Model**:
- Path `user_id` must match JWT `user_id` (enforced in `verify_token_owner`)
- Cross-user access attempts return 404 (not 403) to avoid information leakage
- JWT secret stored in `BETTER_AUTH_SECRET` environment variable

### API Structure

All task endpoints follow pattern: `/api/{user_id}/tasks`

- `GET /api/{user_id}/tasks` - List user's tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion
- `DELETE /api/{user_id}/tasks/{id}` - Delete task

Authentication endpoints: `/api/auth/register`, `/api/auth/login`, `/api/auth/forgot-password`

### Database Schema

**Tasks Table** (`backend/src/models/task_model.py`):
- `id` (primary key)
- `user_id` (indexed, foreign key)
- `title`, `description`, `completed` (indexed)
- `created_at`, `updated_at`

**Users Table**: `user_id` (primary key), `email` (indexed), `created_at`

**Credentials Table**: `user_id`, `password_hash`

**Connection**: PostgreSQL via SQLModel ORM. Connection string in `DATABASE_URL` environment variable.

## Environment Variables

Create `.env` file in root (see `.env.example`):

```bash
# Backend
DATABASE_URL=postgresql://username:password@host:5432/todo_db
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
CORS_ALLOW_ORIGINS=http://localhost:3000

# Frontend
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Spec-Driven Development Workflow

This project follows strict SDD with Spec-Kit Plus. Available commands:

1. `/sp.constitution` - Create/update project constitution
2. `/sp.specify` - Create feature specification
3. `/sp.clarify` - Clarify ambiguous requirements
4. `/sp.plan` - Create implementation plan
5. `/sp.tasks` - Generate actionable tasks
6. `/sp.implement` - Execute implementation
7. `/sp.adr` - Document architectural decisions

**Workflow**: Constitution → Specify → Clarify → Plan → Tasks → Implement

**Artifacts Location**:
- Constitution: `.specify/memory/constitution.md`
- Specs: `specs/<feature>/spec.md`
- Plans: `specs/<feature>/plan.md`
- Tasks: `specs/<feature>/tasks.md`
- ADRs: `history/adr/`
- PHRs: `history/prompts/`

## Key Principles

### Security
- Never trust `user_id` from request body - always use JWT claims
- Enforce ownership at database query level (filter by `user_id`)
- Return 404 for unauthorized access (not 403)
- Validate all inputs with Pydantic models

### Code Organization
- Backend: Separate concerns (models, API routes, middleware, services)
- Frontend: Component-based with clear separation (UI, API client, auth)
- Phase III AI code must be isolated in dedicated directories

### Testing
- Backend: pytest with test database (SQLite in-memory for tests)
- Mock JWT authentication in tests using `unittest.mock.patch`
- Test ownership enforcement and cross-user access scenarios

### Progressive Evolution
- Phase III extends Phase II without modifying frozen artifacts
- Maintain backward compatibility with existing APIs
- AI layer operates through existing API endpoints (no direct DB access)

## Common Patterns

### Backend: Protected Endpoint
```python
@router.get("/tasks")
def get_tasks(
    user_id: str,
    request: Request,
    token: str = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    # Verify token user_id matches path user_id
    token_user_id = request.state.user.get("user_id")
    if token_user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Query with ownership filter
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()
```

### Frontend: API Call with Auth
```typescript
import { apiClient } from '@/lib/api';

// API client automatically attaches JWT from localStorage
const tasks = await apiClient.get<Task[]>(`/${userId}/tasks`);
```

### Testing: Mock JWT
```python
with patch('src.middleware.auth.JWTBearer.__call__') as mock_jwt:
    mock_jwt.return_value = "mock_token"
    with patch('src.middleware.auth.JWTBearer.verify_jwt') as mock_verify:
        mock_verify.return_value = {"user_id": "test-user"}
        # Make test request
```

## Deployment

- **Docker**: Use `docker-compose.yml` for local development with PostgreSQL
- **Production**: Backend expects port 7860 (Hugging Face Spaces compatible)
- **Database**: Neon Serverless PostgreSQL recommended for production

## Important Notes

- Frontend uses Next.js App Router (not Pages Router)
- Backend uses SQLModel (not raw SQLAlchemy)
- Authentication is JWT-based (not session-based)
- CORS configured via `CORS_ALLOW_ORIGINS` environment variable
- Database tables auto-created on startup via `lifespan` function in `main.py`
