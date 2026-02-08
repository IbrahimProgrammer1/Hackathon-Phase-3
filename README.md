# Phase II – Todo Full-Stack Web Application

This repository contains:

- **Phase I (completed / frozen)**: a Python command-line todo application that stores tasks in memory.
- **Phase II (completed / frozen)**: a secure, multi-user full-stack web application with persistent storage.
- **Phase III (current scope)**: an AI-powered conversational assistant integrated into the full-stack web application.

Phase III extends Phase II while strictly preserving all Phase I and Phase II artifacts, specifications, and history.

## Features

### Phase I: Console Application Features
...
### Phase III: AI-Powered Assistant Features
- **Conversational Interface**: Interact with tasks using natural language.
- **Tool-Driven Execution**: Secure translation of user intent into backend API actions.
- **Ownership Enforcement**: AI actions strictly respect user authentication and task ownership.
- **Stateless Reasoning**: AI operates within the context of the user session without persistent external memory.
- Add tasks with title and description
- List all tasks with status indicators (✅ for complete, ⬜ for incomplete)
- Update task details by ID
- Delete tasks by ID
- Mark tasks as complete/incomplete by toggling their status
- In-memory storage (data is lost on exit)
- Input validation and error handling
- Clean, intuitive command-line interface

### Phase II: Full-Stack Web Application Features
- **Multi-user support**: Each user has their own set of tasks
- **Authentication**: Secure login and registration with Better Auth
- **Task management**: Create, read, update, delete, and mark tasks as complete
- **Security**: JWT-based authentication with ownership enforcement
- **Responsive UI**: Works on desktop and mobile devices
- **Persistent Storage**: PostgreSQL database with proper indexing

## Prerequisites

- Node.js 18.17+ or 20.6+ (for frontend)
- Python 3.11+ (for backend)
- PostgreSQL-compatible database (Neon Serverless recommended)

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Update the following variables in .env:
   # DATABASE_URL="your-postgresql-connection-string"
   # BETTER_AUTH_SECRET="your-secret-key-for-jwt-signing"
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### 3. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Update NEXT_PUBLIC_API_BASE_URL to point to your backend
   # NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

### 4. Running Both Services

For development, you can run both services simultaneously:

1. Terminal 1 (Backend):
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

2. Terminal 2 (Frontend):
   ```bash
   cd frontend
   npm run dev
   ```

## Tech Stack

- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: Python FastAPI, SQLModel, python-jose
- **Authentication**: Better Auth
- **Database**: Neon Serverless PostgreSQL
- **Deployment**: Monorepo structure with separate frontend and backend

## API Documentation

The backend API is available at `http://localhost:8000/api/docs` when running in development mode.

## Architecture

The application follows a monorepo structure with separate frontend and backend directories:

```
├── backend/              # FastAPI backend application
│   ├── src/
│   │   ├── models/      # SQLModel database models
│   │   ├── database/    # Database connection
│   │   ├── middleware/  # JWT authentication
│   │   └── api/         # API route definitions
│   └── tests/           # Backend tests
├── frontend/             # Next.js frontend application
│   ├── src/
│   │   ├── app/         # Next.js app router pages
│   │   ├── components/  # Reusable UI components
│   │   ├── lib/         # Utility functions
│   │   └── services/    # Business logic
│   └── tests/           # Frontend tests
├── specs/                # Feature specifications
└── src/                  # Phase I console app (preserved)
```

## Security Features

- JWT-based authentication with 7-day token lifetime
- Ownership enforcement at both API and database layers
- Cross-user access attempts return 404 to avoid information leakage
- All API endpoints require valid JWT tokens
- Path user_id must match JWT user_id for all operations

## Testing

Backend tests:
```bash
cd backend
python -m pytest
```

Frontend tests:
```bash
cd frontend
npm run test
```

## Project Structure (Phase I - Console Application)

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

This project was developed using the Claude Code workflow with Spec-Kit Plus:
1. `/sp.constitution` - Created the project constitution document
2. `/sp.specify` - Created the feature specification document
3. `/sp.clarify` - Clarified ambiguous requirements
4. `/sp.plan` - Created the implementation plan
5. `/sp.tasks` - Broke down the work into actionable tasks
6. `/sp.implement` - Implemented the solution based on all previous artifacts

This workflow ensures that all development is specification-driven, with clear alignment between requirements, architecture, and implementation. Each step builds on the previous one, creating a traceable path from requirements to code.