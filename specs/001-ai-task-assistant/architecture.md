# System Architecture: AI-Powered Conversational Task Assistant

**Feature**: 001-ai-task-assistant | **Date**: 2026-02-11 | **Phase**: III

## Overview

This document defines the system architecture for Phase III AI-powered conversational assistant. The architecture maintains strict separation between the AI interface layer and existing Phase II backend services, ensuring the AI layer is removable without breaking core functionality.

## High-Level Architecture

```
Frontend (Next.js) → AI Chat Endpoint → AI Agent Layer → Tool Executor → Backend APIs → Database
                  ↓                                                    ↓
              Task UI (existing) ────────────────────────────→ Backend APIs → Database
```

**Key Principle**: AI layer is an interface adapter. If removed, system continues via existing REST APIs.

## Component Responsibilities

### Frontend Components

**Chat UI** (NEW - `frontend/src/components/chat/`)
- Render conversation interface
- Manage conversation history (last 10 messages)
- Handle confirmation dialogs
- Propagate JWT with requests

**Task UI** (EXISTING - NO CHANGES)
- Traditional form-based task management
- Direct REST API calls
- Functions independently of AI layer

### Backend Components

**AI Chat Endpoint** (NEW - `backend/src/api/ai_chat.py`)
- Receive chat requests with JWT
- Validate via existing middleware
- Delegate to AI Agent Layer

**AI Agent Layer** (NEW - `backend/src/ai/`)
- Parse natural language with LLM
- Map intent to tool calls
- Enforce system instructions
- Format conversational responses

**Tool Executor** (NEW - `backend/src/ai/tool_executor.py`)
- Validate tool parameters
- Extract and propagate JWT
- Call backend APIs as authenticated proxy
- Handle tool execution errors

**Task API** (EXISTING - NO CHANGES)
- CRUD operations
- JWT validation and ownership enforcement
- Database persistence

## Data Flow: Task Creation

```
User: "Remind me to buy milk"
  ↓
Frontend: Add message, send with JWT + history
  ↓
JWT Middleware: Validate JWT, extract user_id
  ↓
AI Chat Endpoint: Pass to AI Agent
  ↓
AI Agent: LLM returns create_task(title="Buy milk")
  ↓
Tool Executor: Validate params, call POST /api/{user_id}/tasks with JWT
  ↓
Task API: Validate JWT, create task, return Task object
  ↓
AI Agent: Format response "I've created a task: 'Buy milk'"
  ↓
Frontend: Display response
```

## Security Architecture

**Layer 1**: JWT Validation (existing middleware)
**Layer 2**: Tool-Only Execution (no arbitrary code)
**Layer 3**: Ownership Enforcement (backend filters by user_id)
**Layer 4**: Prompt Injection Defense (system instructions + validation)

**Security Checkpoints**:
1. Frontend → Backend: JWT in Authorization header
2. Backend Entry: JWT signature validated, user_id extracted
3. AI Agent: System instructions enforced, suspicious inputs detected
4. Tool Executor: JWT propagated, no user_id in parameters
5. Backend APIs: JWT re-validated, queries filtered by user_id

## JWT Propagation Pattern

```python
# Frontend
headers: {'Authorization': `Bearer ${jwt}`}

# AI Chat Endpoint
user_id = request.state.user.get("user_id")  # From JWT

# Tool Executor
headers = {"Authorization": f"Bearer {jwt}"}
response = await http_client.post(f"/api/{user_id}/tasks", headers=headers)
```

## Stateless Conversation

- Frontend manages last 10 messages
- Backend processes each request independently
- No conversation state stored in backend
- Enables horizontal scaling

## Removal Test

**Verification**: Delete AI components → Existing task UI still works ✅

Components to remove:
- `backend/src/ai/`
- `backend/src/api/ai_chat.py`
- `frontend/src/components/chat/`
- `frontend/src/app/chat/`

Result: Task CRUD via REST API continues to function.

## Performance Targets

- AI response latency: < 2.0s (p95)
- Tool execution: < 500ms (p95)
- End-to-end turn: < 2.5s (p95)

**Optimizations**:
- Concise system prompts
- Cached tool schemas
- Parallel tool execution
- Aggressive timeouts

## Monitoring

**Key Metrics**:
- AI response latency (p50, p95, p99)
- Tool execution time
- LLM API error rate
- JWT validation failure rate
- Cross-user access attempts (should be 0)

## Architecture Validation

✅ Clear separation of concerns
✅ AI layer isolated and removable
✅ Security enforced at multiple layers
✅ Stateless backend design
✅ JWT propagation maintains Phase II security
✅ No database schema changes
✅ No business logic in AI layer
✅ Ready for implementation
