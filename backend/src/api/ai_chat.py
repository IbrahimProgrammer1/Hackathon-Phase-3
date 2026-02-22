"""
AI Chat Endpoint for Task Management Assistant

This module provides the REST API endpoint for conversational task management.
It integrates JWT authentication with the AI agent to provide secure,
conversational access to task operations.

Constitutional Requirements:
- JWT authentication required for all requests
- user_id extracted from JWT claims (never from request body)
- Stateless processing (no conversation state stored)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from ..middleware.auth import JWTBearer
from ..ai.agent import AIAgent


# T027: Define ChatRequest model
class ConversationMessage(BaseModel):
    """Single message in conversation history."""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(
        min_length=1,
        max_length=2000,
        description="User's current message"
    )
    conversation_history: List[ConversationMessage] = Field(
        default=[],
        max_items=10,
        description="Previous conversation messages (last 10)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Create a task to buy milk",
                "conversation_history": [
                    {
                        "role": "user",
                        "content": "Show me my tasks",
                        "timestamp": "2026-02-16T12:00:00Z"
                    },
                    {
                        "role": "assistant",
                        "content": "You have 3 tasks...",
                        "timestamp": "2026-02-16T12:00:01Z"
                    }
                ]
            }
        }


# T028: Define ChatResponse model
class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    message: str = Field(description="AI assistant's response")
    requires_confirmation: bool = Field(
        default=False,
        description="Whether user confirmation is required"
    )
    confirmation_details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Details about what needs confirmation"
    )
    tool_calls: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Tools that were called (for debugging)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "I've created a task: 'Buy milk'",
                "requires_confirmation": False,
                "confirmation_details": None,
                "tool_calls": [
                    {
                        "name": "create_task",
                        "parameters": {
                            "title": "Buy milk"
                        }
                    }
                ]
            }
        }


# T024: Create AI chat endpoint
router = APIRouter(prefix="/api", tags=["ai-chat"])

# Initialize AI agent (singleton)
ai_agent = None


def get_ai_agent() -> AIAgent:
    """Get or create AI agent instance."""
    global ai_agent
    if ai_agent is None:
        ai_agent = AIAgent()
    return ai_agent


# T029: Implement chat endpoint handler
@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: Request,
    chat_request: ChatRequest,
    token: str = Depends(JWTBearer())  # T025: JWT validation
):
    """
    Process a conversational message and return AI response.

    This endpoint:
    1. Validates JWT token (via JWTBearer dependency)
    2. Extracts user_id from JWT claims
    3. Processes message with AI agent
    4. Returns conversational response

    Security:
    - JWT required for all requests
    - user_id derived from JWT (never from request body)
    - All tool executions use authenticated user_id

    Args:
        request: FastAPI request object (contains JWT claims in state)
        chat_request: User's message and conversation history
        token: JWT token (validated by JWTBearer)

    Returns:
        ChatResponse with AI's message and metadata

    Raises:
        HTTPException: If authentication fails or processing errors occur
    """
    try:
        # T026: Extract user_id from JWT claims
        if not hasattr(request.state, 'user'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User information not found in token"
            )

        user_id = request.state.user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token"
            )

        # Get AI agent
        agent = get_ai_agent()

        # Convert conversation history to dict format
        history = [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat() if msg.timestamp else None
            }
            for msg in chat_request.conversation_history
        ]

        # Process message with AI agent
        response = agent.process(
            message=chat_request.message,
            conversation_history=history,
            jwt=token,
            user_id=user_id
        )

        # Return response
        return ChatResponse(
            message=response.get("message", "I'm having trouble processing that request."),
            requires_confirmation=response.get("requires_confirmation", False),
            confirmation_details=response.get("confirmation_details"),
            tool_calls=response.get("tool_calls")
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log error with full traceback for debugging
        import traceback
        print(f"Chat endpoint error: {str(e)}")
        print(traceback.format_exc())

        # Return more specific error message based on exception type
        error_detail = str(e)
        if "timeout" in error_detail.lower():
            user_message = "The request took too long. Please try again."
        elif "connection" in error_detail.lower():
            user_message = "Unable to connect to the server. Please try again."
        elif "JWT" in error_detail or "token" in error_detail.lower():
            user_message = "Authentication error. Please log in again."
        else:
            user_message = "I'm having trouble processing your request right now. Please try again in a moment."

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=user_message
        )


@router.get("/chat/health")
async def chat_health():
    """
    Health check endpoint for AI chat service.

    Returns:
        Status information about the AI service
    """
    try:
        agent = get_ai_agent()
        return {
            "status": "healthy",
            "provider": agent.provider,
            "model": agent.model,
            "tools_available": len(agent.tools)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
