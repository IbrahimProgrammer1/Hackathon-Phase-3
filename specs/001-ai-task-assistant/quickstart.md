# Quickstart: AI Task Assistant

## Development Setup

1. **Environment Variables**:
   Add the following to `backend/.env`:
   ```env
   OPENAI_API_KEY=your_key_here
   AI_MODEL=gpt-4-turbo-preview
   ```

2. **Backend API**:
   The AI agent endpoint is available at `POST /api/v1/ai/chat`.
   It expects a JSON body:
   ```json
   {
     "messages": [
       {"role": "user", "content": "What are my tasks?"}
     ]
   }
   ```

3. **Frontend Integration**:
   - Use the `ChatWidget` component in `frontend/src/components/chat/ChatWidget.tsx`.
   - Ensure the user is authenticated; the widget will automatically pull the JWT from the auth context.

## Testing the AI
1. Run backend: `uvicorn main:app --reload`
2. Open Swagger UI: `http://localhost:8000/api/docs`
3. Authorize with a JWT.
4. Send a request to `/api/v1/ai/chat`.
