from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List
from sqlmodel import Session, select
from pydantic import BaseModel
from ..database import get_session
from ..models.task_model import Task, TaskBase
from ..middleware.auth import JWTBearer


# Pydantic model for task completion update request body
class TaskCompletionUpdate(BaseModel):
    completed: bool


router = APIRouter(prefix="/api/{user_id}", tags=["tasks"])

# GET /api/{user_id}/tasks
@router.get("/tasks", response_model=List[Task])
def get_tasks(user_id: str, request: Request, token: str = Depends(JWTBearer()), session: Session = Depends(get_session)):
    # Verify that the user_id in the JWT matches the user_id in the path
    token_user_id = request.state.user.get("user_id")
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match path parameter"
        )

    # Query tasks for the authenticated user
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks


# POST /api/{user_id}/tasks
@router.post("/tasks", response_model=Task)
def create_task(user_id: str, task: TaskBase, request: Request, token: str = Depends(JWTBearer()), session: Session = Depends(get_session)):
    # Verify token owner
    token_user_id = request.state.user.get("user_id")
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match path parameter"
        )

    # Create new task with user_id
    db_task = Task(**task.dict(), user_id=user_id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


# GET /api/{user_id}/tasks/{task_id}
@router.get("/tasks/{task_id}", response_model=Task)
def get_task(user_id: str, task_id: int, request: Request, token: str = Depends(JWTBearer()), session: Session = Depends(get_session)):
    # Verify token owner
    token_user_id = request.state.user.get("user_id")
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match path parameter"
        )

    # Get specific task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )
    return db_task


# PUT /api/{user_id}/tasks/{task_id}
@router.put("/tasks/{task_id}", response_model=Task)
def update_task(user_id: str, task_id: int, task: TaskBase, request: Request, token: str = Depends(JWTBearer()), session: Session = Depends(get_session)):
    # Verify token owner
    token_user_id = request.state.user.get("user_id")
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match path parameter"
        )

    # Get and update task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    # Update task fields
    for field, value in task.dict().items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


# DELETE /api/{user_id}/tasks/{task_id}
@router.delete("/tasks/{task_id}")
def delete_task(user_id: str, task_id: int, request: Request, token: str = Depends(JWTBearer()), session: Session = Depends(get_session)):
    # Verify token owner
    token_user_id = request.state.user.get("user_id")
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match path parameter"
        )

    # Get and delete task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    session.delete(db_task)
    session.commit()
    return {"message": "Task deleted successfully"}


# PATCH /api/{user_id}/tasks/{task_id}/complete
@router.patch("/tasks/{task_id}/complete", response_model=Task)
def toggle_task_completion(user_id: str, task_id: int, completion_data: TaskCompletionUpdate, request: Request, token: str = Depends(JWTBearer()), session: Session = Depends(get_session)):
    # Verify token owner
    token_user_id = request.state.user.get("user_id")
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match path parameter"
        )

    # Get and update task completion status
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    db_task.completed = completion_data.completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task