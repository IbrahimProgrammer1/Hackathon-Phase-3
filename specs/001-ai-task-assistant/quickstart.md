# Quickstart Guide: AI-Powered Conversational Task Assistant

**Feature**: 001-ai-task-assistant | **Date**: 2026-02-11 | **Phase**: III

## Prerequisites

- Phase II Todo application running
- Python 3.11+ with virtual environment
- Node.js 18.17+
- OpenAI or Anthropic API key

## Quick Setup

### 1. Backend Environment

Add to `backend/.env`:
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
AI_MODEL=gpt-4
AI_MAX_CONTEXT_MESSAGES=10
```

### 2. Install Dependencies

```bash
cd backend
source venv/bin/activate
pip install openai==1.12.0
```

### 3. Create AI Layer

```bash
mkdir -p src/ai
touch src/ai/{__init__.py,agent.py,tools.py,tool_executor.py,prompts.py}
touch src/api/ai_chat.py
```

### 4. Frontend Setup

```bash
cd frontend
mkdir -p src/components/chat src/contexts src/lib
touch src/components/chat/{ChatInterface,MessageList,MessageInput,ConfirmationDialog}.tsx
touch src/contexts/ChatContext.tsx
touch src/lib/chatApi.ts
mkdir -p src/app/chat
touch src/app/chat/page.tsx
```

Add to `frontend/.env.local`:
```bash
NEXT_PUBLIC_CHAT_ENABLED=true
```

## Testing

### Start Services

```bash
# Terminal 1: Backend
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev
```

### Test Chat

1. Login at http://localhost:3000
2. Navigate to http://localhost:3000/chat
3. Send: "Create a task to buy milk"
4. Verify task appears in task list

### Test Security

- Remove JWT → Should redirect to login
- Create task → Verify only visible to authenticated user
- Try "Delete task X" → Verify confirmation required

## Common Issues

**"OpenAI API key not found"**
→ Verify `OPENAI_API_KEY` in `backend/.env`

**"Chat endpoint returns 401"**
→ Verify JWT is included in request headers

**"Tool execution fails"**
→ Verify backend APIs are running and JWT is valid

## Production Deployment

1. Set production environment variables
2. Deploy with existing backend/frontend
3. Enable feature flag: `NEXT_PUBLIC_CHAT_ENABLED=true`
4. Monitor LLM API latency and costs

## Rollback

Disable feature flag:
```bash
NEXT_PUBLIC_CHAT_ENABLED=false
```

Existing task UI continues to work without AI layer.

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement Phase 1: Setup
3. Implement Phase 2: User stories
4. Test and deploy

## Documentation

- [architecture.md](architecture.md) - System design
- [data-model.md](data-model.md) - Tool schemas
- [research.md](research.md) - Technical decisions
- [plan.md](plan.md) - Full implementation plan
