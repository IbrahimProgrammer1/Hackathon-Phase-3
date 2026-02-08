# Research: AI-Powered Task Assistant

## Phase 0: Technical Research

### 1. LLM Tool/Function Calling Patterns
**Decision**: Use OpenAI Function Calling (or compatible provider) via structured Pydantic models in FastAPI.
**Rationale**: Pydantic models provide native validation in FastAPI and can be easily converted to JSON schemas for the LLM. This ensures type safety between the LLM output and our backend services.
**Alternatives Considered**: LangChain Agents (rejected for being too heavyweight for simple CRUD), manual regex parsing (rejected as brittle).

### 2. Stateless Agent Execution
**Decision**: Client-side history management. The frontend will send the last N messages with each request. The backend will remain stateless.
**Rationale**: Aligns with Phase III constitution. No need for complex server-side session management or memory databases.
**Alternatives Considered**: Redis-based session storage (rejected for complexity), no history (rejected as it breaks conversational UX).

### 3. Secure JWT Propagation
**Decision**: The AI endpoint will be protected by the existing Phase II JWT middleware. The `user_id` will be extracted from the token and passed directly to the task services called by the tools.
**Rationale**: Ensures that even if the AI is "hallucinating" a user ID, the backend only operates on the ID verified by the cryptographic token.
**Alternatives Considered**: AI "knowing" the user ID (rejected as it relies on AI honesty).

### 4. Tool Mapping
- `create_task(title: str, description: str)` -> calls `TaskService.create_task`
- `list_tasks(status: Optional[str])` -> calls `TaskService.get_user_tasks`
- `update_task(task_id: int, title: str, description: str)` -> calls `TaskService.update_task`
- `delete_task(task_id: int)` -> calls `TaskService.delete_task`
- `toggle_task(task_id: int, completed: bool)` -> calls `TaskService.toggle_task`
