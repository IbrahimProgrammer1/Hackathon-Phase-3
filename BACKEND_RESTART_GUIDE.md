# Backend Server Restart Instructions

## Problem
Multiple old backend server instances are running, causing 404 errors for auth and tasks endpoints.

## Solution

### Windows Users:

1. **Stop all backend processes:**
   ```cmd
   taskkill /F /IM python.exe
   ```

2. **Navigate to backend directory:**
   ```cmd
   cd backend
   ```

3. **Start fresh backend server:**
   ```cmd
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   OR use the provided script:
   ```cmd
   restart_backend.bat
   ```

### Verify Backend is Working:

1. **Check health endpoint:**
   ```bash
   curl http://localhost:8000/health
   ```
   Expected: `{"status":"healthy",...}`

2. **Check auth register endpoint:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"name":"Test","email":"test@test.com","password":"test123"}'
   ```
   Expected: `{"token":"...","user":{...}}`

3. **View all available routes:**
   Open browser: http://localhost:8000/docs

### Frontend Setup:

1. **Check environment variable:**
   Create/update `frontend/.env.local`:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_CHAT_ENABLED=true
   ```

2. **Start frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test registration:**
   - Go to http://localhost:3000/auth/register
   - Fill in the form
   - Should successfully register and redirect to /tasks

## Common Issues:

### Issue: "Port 8000 already in use"
**Solution:** Kill all Python processes first:
```cmd
taskkill /F /IM python.exe
```

### Issue: "404 Not Found" for /api/auth/register
**Solution:** Backend server is running old code. Restart it using steps above.

### Issue: Frontend can't connect to backend
**Solution:** Check CORS settings in backend/.env:
```
CORS_ALLOW_ORIGINS=http://localhost:3000
```

## Expected Behavior After Fix:

✓ Registration works at /auth/register
✓ Login works at /auth/login
✓ Tasks page loads at /tasks
✓ Chat page loads at /chat (if NEXT_PUBLIC_CHAT_ENABLED=true)
✓ All API calls return proper responses (not 404)
