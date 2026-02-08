# Quickstart Guide: Phase II Todo Full-Stack Web App

## Prerequisites

- Node.js 18.17+ or 20.6+ (LTS recommended)
- Python 3.11+
- PostgreSQL-compatible database (Neon Serverless recommended)
- Better Auth account for frontend authentication

## Environment Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Set up environment variables:
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Update the following variables in .env:
   BETTER_AUTH_SECRET="your-secret-key-for-jwt-signing"
   DATABASE_URL="your-postgresql-connection-string"
   ```

## Backend Setup (FastAPI + SQLModel)

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
   pip install fastapi sqlmodel python-jose uvicorn psycopg2-binary
   ```

4. Run database migrations (if applicable):
   ```bash
   # This will depend on your migration setup
   # Example: alembic upgrade head
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## Frontend Setup (Next.js + Better Auth)

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

3. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. The frontend will be available at `http://localhost:3000`

## Running Both Services

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

## API Testing

With both services running, you can test the API endpoints directly at:
- Backend API: `http://localhost:8000/api/docs` (Swagger UI)
- Frontend: `http://localhost:3000`

## Database Migrations

If using Alembic for migrations:
```bash
# Generate a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head
```

## Running Tests

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