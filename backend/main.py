from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from dotenv import load_dotenv
import os

# Load environment variables FIRST, before any database imports
load_dotenv()
load_dotenv('.env.local')  # Also load from backend directory

from src.database import engine
from src.api.tasks import router as tasks_router
from src.api.auth import router as auth_router
from src.api.ai_chat import router as ai_chat_router
from src.api.error_handlers import add_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    print("Checking database connection...")
    try:
        # Import all models to ensure they're registered with SQLModel
        from src.models.task_model import Task, User, Credential, PasswordResetToken
        SQLModel.metadata.create_all(engine)
        print("Database tables verified/created.")
    except Exception as e:
        print(f"Error during database initialization: {e}")
        # We don't raise the error here so the app can still start 
        # and show a health check, allowing Hugging Face to see it's "live"
    yield
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Todo API",
    description="Secure, multi-user todo application API with JWT authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
# NOTE: Using allow_credentials=True with allow_origins=["*"] breaks browser CORS.
# We use explicit origins (comma-separated) and do not rely on cookies for auth.
allow_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Add exposed headers to allow frontend to access custom response headers
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"]
)

# Include API routers
app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(ai_chat_router)  # T030: Register AI chat router

# Add exception handlers
add_exception_handlers(app)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-api"}


if __name__ == "__main__":
    import uvicorn
    # Hugging Face Spaces uses port 7860 by default
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run(app, host="0.0.0.0", port=port)