"""
Debug server to verify database configuration at runtime
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from src.database import engine, DATABASE_URL  # This will load at import time
import os
from dotenv import load_dotenv

# Load environment variables - make sure this happens before anything else
load_dotenv('.env.local')
print(f"DATABASE_URL at import time: {DATABASE_URL}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    print(f"Starting server with DATABASE_URL: {DATABASE_URL}")

    if DATABASE_URL.startswith("postgresql"):
        print("✓ Using PostgreSQL (Neon) database")
    else:
        print("⚠ Using fallback SQLite database")

    # Import all models to ensure they're registered with SQLModel
    from src.models.task_model import Task, User, Credential, PasswordResetToken
    SQLModel.metadata.create_all(engine)
    print("Database tables created/verified.")
    yield
    # Cleanup on shutdown if needed
    print("Shutting down...")

# Create FastAPI app
app = FastAPI(
    title="Todo API - Debug Mode",
    description="Debug version to verify database configuration",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "Database URL", "database_url": DATABASE_URL, "is_postgres": DATABASE_URL.startswith("postgresql")}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database_url": DATABASE_URL, "is_postgres": DATABASE_URL.startswith("postgresql")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)