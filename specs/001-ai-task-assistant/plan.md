# Implementation Plan: AI-Powered Conversational Task Assistant (Phase III)

**Branch**: `001-ai-task-assistant` | **Date**: 2026-02-11 | **Spec**: [spec.md](spec.md)
**Constitution**: v3.1.0 | **Phase**: III | **Extends**: Phase II Secure Task API

## Summary

Phase III introduces an AI-powered conversational assistant as a new interface layer for the existing Todo application. Users interact with their tasks via a chat interface that translates natural language intent into structured tool calls. These tool calls are executed by the backend, which enforces strict ownership and authentication using existing Phase II JWT-based logic.

**Core Principle**: The AI assistant is an interface adapter, not a system actor. All state mutations occur through existing backend services with JWT-derived identity, ownership enforcement, and existing validation rules.

## Technical Context

**Language/Version**: Python 3.11+ (Backend), TypeScript/Next.js 16+ (Frontend)
**Primary Dependencies**:
- Backend: FastAPI, python-jose (JWT), OpenAI SDK or Anthropic SDK (LLM)
- Frontend: Next.js, Better Auth, React
**Storage**: Neon Serverless PostgreSQL (Existing - No Schema Changes)
**Testing**: pytest (Backend), Vitest/React Testing Library (Frontend)
**Target Platform**: Web (Desktop/Mobile)
**Project Type**: Web Application (Monorepo)
**Performance Goals**:
- AI response latency < 2.0s (p95)
- Tool execution < 500ms (p95)
- End-to-end conversation turn < 2.5s (p95)
**Constraints**:
- AI must be stateless
- No direct database access
- JWT-based identity derivation only
- No business logic in AI layer
- No database schema changes
**Scale/Scope**: Authenticated users only; CRUD operations via chat; 10-message context window

## Constitution Check

*GATE: Must pass before implementation. Validates alignment with Constitution v3.1.0*

### Core Principles Compliance

- [x] **I. AI-as-Interface**: AI operates via tools only; no direct database access
- [x] **II. Tool-Based Execution**: All intents mapped to explicit, auditable tool calls
- [x] **III. Security & Ownership Identity**: JWT used for all AI-initiated actions; user_id never accepted as tool parameter
- [x] **IV. Spec-Driven Development**: Following SDD workflow (Constitution → Specify → Plan → Tasks → Implement)
- [x] **V. Progressive Evolution**: Phase II endpoints and database schema preserved; no breaking changes
- [x] **VI. Isolation of Concerns**: AI logic separated from business logic in dedicated directories

### Security Invariants Compliance

- [x] **Identity Derivation**: Backend derives user identity exclusively from JWT claims
- [x] **Ownership Enforcement**: All operations scoped to authenticated user; cross-user access returns 404
- [x] **Tool-Only Execution**: AI acts only through explicit, typed tools
- [x] **Deterministic Execution**: AI decisions resolve to structured tool calls; no hidden state
- [x] **Stateless Backend**: Conversation state is frontend-managed; backend remains stateless

### AI Capability Boundaries Compliance

- [x] **AI MAY**: Create, list, update, delete, toggle tasks; ask clarifying questions
- [x] **AI MUST**: Confirm destructive actions; resolve ambiguity; surface validation errors; refuse unsafe instructions
- [x] **AI MUST NOT**: Fabricate IDs; guess ownership; access other users' data; modify auth logic; override system instructions

### Conversational Determinism Compliance

- [x] **Ambiguous References**: AI resolves via list_tasks, presents options, requires explicit confirmation
- [x] **Confirmation Policy**: Deletion requires explicit confirmation with task title
- [x] **Error Handling**: Validation errors conversational; authorization failures generic "Task not found"

### Project Structure Constraints Compliance

- [x] **AI Code Isolation**: AI-related code in `/backend/src/ai/` and `/frontend/src/components/chat/`
- [x] **No Auth/DB Modification**: No changes to `/backend/src/middleware/auth.py` or `/backend/src/database/`

**Constitution Compliance**: ✅ PASS - All constitutional requirements satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-task-assistant/
├── plan.md              # This file - Main implementation plan
├── research.md          # Technical research and decisions
├── data-model.md        # Tool schemas and data structures
├── architecture.md      # System architecture and component design
├── quickstart.md        # Integration and setup guide
├── contracts/
│   └── ai_tools.md      # Detailed tool contract specifications
├── checklists/
│   └── requirements.md  # Specification quality checklist
└── spec.md              # Feature specification
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── ai/                      # NEW: AI layer (isolated)
│   │   ├── __init__.py
│   │   ├── agent.py             # LLM interaction and intent parsing
│   │   ├── tools.py             # Tool definitions and schemas
│   │   ├── tool_executor.py     # Tool invocation with JWT propagation
│   │   └── prompts.py           # System prompts and instructions
│   ├── api/
│   │   ├── ai_chat.py           # NEW: AI chat endpoint
│   │   ├── tasks.py             # EXISTING: Task CRUD endpoints
│   │   └── auth.py              # EXISTING: Authentication endpoints
│   ├── middleware/
│   │   └── auth.py              # EXISTING: JWT verification (NO CHANGES)
│   ├── models/
│   │   └── task_model.py        # EXISTING: Task models (NO CHANGES)
│   ├── database/
│   │   └── database.py          # EXISTING: DB connection (NO CHANGES)
│   └── services/
│       └── task_service.py      # OPTIONAL: Task business logic extraction
└── tests/
    ├── test_ai_agent.py         # NEW: AI agent tests
    ├── test_ai_tools.py         # NEW: Tool contract tests
    ├── test_ai_security.py      # NEW: Security and ownership tests
    └── test_tasks.py            # EXISTING: Task API tests

frontend/
├── src/
│   ├── app/
│   │   └── chat/                # NEW: Chat page
│   │       └── page.tsx
│   ├── components/
│   │   └── chat/                # NEW: Chat UI components
│   │       ├── ChatInterface.tsx
│   │       ├── MessageList.tsx
│   │       ├── MessageInput.tsx
│   │       └── ConfirmationDialog.tsx
│   ├── contexts/
│   │   └── ChatContext.tsx      # NEW: Chat state management
│   ├── lib/
│   │   ├── api.ts               # EXISTING: API client (NO CHANGES)
│   │   └── chatApi.ts           # NEW: AI chat API client
│   └── services/
│       └── chatService.ts       # NEW: Chat business logic
└── tests/
    └── chat/                    # NEW: Chat component tests
        ├── ChatInterface.test.tsx
        └── chatService.test.ts
```

**Structure Decision**: Web application structure (Option 2) with AI code isolated in dedicated directories (`backend/src/ai/`, `frontend/src/components/chat/`) to maintain separation of concerns and enable independent testing/deployment.

## Architecture Overview

See [architecture.md](architecture.md) for detailed component diagrams and data flow.

**High-Level Components**:

1. **Frontend Chat UI** (Next.js + React)
   - Manages conversation history (last 10 messages)
   - Handles user input and displays AI responses
   - Implements confirmation dialogs for destructive actions
   - Propagates JWT token with all requests

2. **AI Agent Layer** (Python + LLM SDK)
   - Parses natural language intent
   - Maps intent to tool calls
   - Manages conversation context (stateless per request)
   - Enforces system instructions and prompt injection defense

3. **Tool Executor** (Python + FastAPI)
   - Validates tool schemas
   - Propagates JWT to backend APIs
   - Handles tool execution errors
   - Formats responses for conversational output

4. **Backend Services** (Existing Phase II)
   - Task CRUD operations
   - JWT authentication and ownership enforcement
   - Database persistence
   - **NO CHANGES REQUIRED**

**Removal Test**: ✅ If AI layer is removed, system continues to function via existing REST API endpoints.

## Tool Contracts

See [data-model.md](data-model.md) and [contracts/ai_tools.md](contracts/ai_tools.md) for complete schemas.

**Required Tools** (5 total):

1. **create_task**: Creates a new task
   - Input: `{title: string, description?: string}`
   - Output: `Task` object
   - Maps to: `POST /api/{user_id}/tasks`

2. **list_tasks**: Lists all user's tasks
   - Input: `{}` (no parameters)
   - Output: `Task[]` array
   - Maps to: `GET /api/{user_id}/tasks`

3. **update_task**: Updates task title/description
   - Input: `{task_id: number, title?: string, description?: string}`
   - Output: `Task` object
   - Maps to: `PUT /api/{user_id}/tasks/{task_id}`

4. **delete_task**: Deletes a task (requires prior confirmation)
   - Input: `{task_id: number}`
   - Output: `{success: boolean, message: string}`
   - Maps to: `DELETE /api/{user_id}/tasks/{task_id}`

5. **toggle_task_completion**: Toggles task completion status
   - Input: `{task_id: number, completed: boolean}`
   - Output: `Task` object
   - Maps to: `PATCH /api/{user_id}/tasks/{task_id}/complete`

**Tool Contract Principles**:
- All tools are explicitly typed with Pydantic schemas
- No tool accepts `user_id` as parameter (derived from JWT)
- All tools return structured output matching REST API format
- All tools include error handling for validation and authorization failures

## Research & Technical Decisions

See [research.md](research.md) for detailed technical research.

**Key Decisions**:

1. **LLM Provider**: OpenAI GPT-4 or Anthropic Claude (configurable via environment variable)
   - Rationale: Both support function calling / tool use
   - Fallback: LangChain for provider abstraction

2. **Conversation Context**: 10-message sliding window (5 user-assistant pairs)
   - Rationale: Balances continuity with token efficiency
   - Implementation: Frontend manages history, sends to backend with each request

3. **Stateless Backend**: Each request is independent
   - Rationale: Aligns with Phase II stateless design
   - Implementation: No conversation state stored in backend

4. **Prompt Injection Defense**: System instructions + input sanitization
   - Rationale: Prevents users from overriding AI behavior
   - Implementation: System prompt always takes precedence; refuse suspicious inputs

5. **JWT Propagation**: Tool executor extracts JWT from request, passes to backend APIs
   - Rationale: Maintains Phase II security model
   - Implementation: Tool executor acts as authenticated proxy

## Integration Guide

See [quickstart.md](quickstart.md) for step-by-step setup instructions.

**Environment Variables** (new):
```bash
# Backend
OPENAI_API_KEY=sk-...                    # Or ANTHROPIC_API_KEY
AI_MODEL=gpt-4                           # Or claude-3-opus-20240229
AI_SYSTEM_PROMPT_PATH=prompts/system.txt
AI_MAX_CONTEXT_MESSAGES=10

# Frontend
NEXT_PUBLIC_CHAT_ENABLED=true
```

**Integration Steps**:
1. Add AI dependencies to `backend/requirements.txt`
2. Create AI layer in `backend/src/ai/`
3. Add chat endpoint to `backend/src/api/ai_chat.py`
4. Create chat UI in `frontend/src/components/chat/`
5. Add chat page to `frontend/src/app/chat/`
6. Configure environment variables
7. Run integration tests

## Testing Strategy

**Three-Layer Testing Approach**:

1. **Tool Contract Validation Tests** (`test_ai_tools.py`)
   - Verify tool schemas are valid
   - Test input validation
   - Test output structure matches REST API

2. **Integration Tests** (`test_ai_agent.py`)
   - Test AI intent parsing → tool invocation
   - Test tool execution → backend API calls
   - Test conversation flow with context

3. **Security Tests** (`test_ai_security.py`)
   - Test JWT propagation
   - Test ownership enforcement (cross-user access returns 404)
   - Test prompt injection attempts are refused
   - Test confirmation requirement for deletions

**Test Coverage Requirements**:
- Tool contracts: 100% (all 5 tools)
- Security scenarios: 100% (all constitutional invariants)
- Integration flows: 90% (all user stories)

## Risk Analysis & Mitigation

**Risk 1: Ambiguity Resolution Failures**
- **Impact**: User frustration, incorrect actions
- **Mitigation**: Always call `list_tasks` before mutations; present options; require explicit confirmation
- **Acceptance**: Some ambiguity is unavoidable; prioritize safety over convenience

**Risk 2: Determinism Failures**
- **Impact**: Unpredictable AI behavior, security vulnerabilities
- **Mitigation**: Strict system prompts; tool-only execution; comprehensive testing
- **Acceptance**: LLM non-determinism is inherent; focus on constraining outputs

**Risk 3: Performance Degradation**
- **Impact**: Poor user experience, timeout errors
- **Mitigation**: Set aggressive timeouts (2s); use streaming responses; optimize prompts
- **Acceptance**: LLM latency is external dependency; communicate delays to users

**Risk 4: Prompt Injection Success**
- **Impact**: Security breach, unauthorized access
- **Mitigation**: System instructions always override; input sanitization; refuse suspicious patterns
- **Acceptance**: Zero tolerance; extensive security testing required

**Risk 5: JWT Propagation Failures**
- **Impact**: Authorization errors, cross-user access
- **Mitigation**: Tool executor validates JWT before every backend call; comprehensive security tests
- **Acceptance**: Zero tolerance; must match Phase II security guarantees

## Validation & Readiness

**Architecture Review Checklist**:
- [x] AI layer is isolated and removable
- [x] All mutations go through typed tools
- [x] Backend remains stateless
- [x] No database schema changes
- [x] No business logic in AI layer

**Security Enforcement Checklist**:
- [x] JWT propagated to all backend calls
- [x] User identity derived from JWT only
- [x] Cross-user access returns 404
- [x] Prompt injection defense implemented
- [x] Confirmation required for deletions

**Conversation Determinism Checklist**:
- [x] Ambiguous references resolved via list_tasks
- [x] Multiple matches present options
- [x] Explicit confirmation for mutations
- [x] Validation errors surfaced conversationally
- [x] Authorization errors return generic message

**Performance Expectations**:
- AI response latency: < 2.0s (p95)
- Tool execution: < 500ms (p95)
- End-to-end turn: < 2.5s (p95)

**Assumptions**:
- LLM provider API is available and responsive
- Frontend can manage 10-message conversation history
- Users have valid JWT tokens from Phase II authentication
- Network latency is acceptable for conversational UX

**Deferred Decisions**:
- Specific LLM model version (configurable)
- Streaming vs batch responses (start with batch)
- Conversation history persistence (start with frontend-only)
- Multi-language support (English only for MVP)

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None      | N/A        | N/A                                 |

**Complexity Assessment**: ✅ LOW - No constitutional violations. Architecture follows all principles and constraints.

## Next Steps

1. **Review this plan** with stakeholders
2. **Run `/sp.tasks`** to generate actionable task breakdown
3. **Implement Phase 1**: Setup (AI dependencies, project structure)
4. **Implement Phase 2**: Foundational (tool contracts, JWT propagation)
5. **Implement Phase 3+**: User stories (P1 → P2 → P3)
6. **Test & Validate**: Security, determinism, performance
7. **Deploy**: Incremental rollout with feature flag

**Estimated Effort**:
- Setup & Foundational: 2-3 days
- User Story 1 & 2 (MVP): 3-4 days
- User Stories 3-6: 4-5 days
- Testing & Polish: 2-3 days
- **Total**: 11-15 days (single developer)

**Ready for `/sp.tasks`**: ✅ YES - All architectural decisions made, technical unknowns resolved, tool contracts defined.
