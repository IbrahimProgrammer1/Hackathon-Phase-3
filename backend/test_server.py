from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from backend.src.database import engine
from backend.src.api.tasks import router as tasks_router
from backend.src.api.auth import router as auth_router
from backend.src.api.error_handlers import add_exception_handlers
import os
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    print("Creating database tables...")
    print("Importing models...")

    # Import all models to ensure they're registered with SQLModel
    from backend.src.models.task_model import Task, User, Credential, PasswordResetToken

    SQLModel.metadata.create_all(engine)
    print("Database tables created.")
    yield
    # Cleanup on shutdown if needed
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
    uvicorn.run(app, host="0.0.0.0", port=8000)