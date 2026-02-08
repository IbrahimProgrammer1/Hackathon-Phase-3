# Claude Code Rules - Frontend

This file defines the frontend-specific rules and conventions for the Phase II Todo Full-Stack Web Application.

## Task context

**Your Surface:** You operate on frontend-specific implementation tasks for the Todo application.

**Your Success is Measured By:**
- All frontend code follows React/Next.js best practices
- User authentication flows work seamlessly
- API calls are properly authenticated with JWT
- UI is responsive and user-friendly
- Frontend-backend integration is seamless

## Frontend Architecture

### Technology Stack
- Next.js 16+ with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- Better Auth for authentication
- React Hooks for state management

### Project Structure
```
frontend/
├── src/
│   ├── app/              # Next.js app router pages
│   │   ├── auth/         # Authentication pages
│   │   └── tasks/        # Task management pages
│   ├── components/       # Reusable UI components
│   ├── lib/              # Utility functions and API client
│   │   ├── api.ts        # API client with JWT handling
│   │   └── auth.ts       # Authentication service
│   └── services/         # Business logic services
├── public/               # Static assets
├── tests/                # Frontend tests
└── package.json          # Dependencies
```

### API Integration
- All API calls must include JWT in Authorization header
- Error responses follow the format: `{ error: "message", code: status_code }`
- Cross-user access attempts return 404 (not found) to avoid leaking information

### Authentication Flow
- Use Better Auth for signup/login
- Store JWT securely in localStorage (or HTTP-only cookies in production)
- Redirect to login when authentication is required
- Handle token expiration scenarios

## Development Guidelines

### 1. Security First
- Never trust client-side user_id alone
- Always verify authentication state before API calls
- Properly handle 401, 403, and 404 responses
- Sanitize user inputs before sending to backend

### 2. User Experience
- Provide loading states for all async operations
- Display clear error messages to users
- Ensure responsive design across devices
- Implement proper form validation

### 3. Code Quality
- Use TypeScript for all components
- Follow Next.js best practices for routing
- Implement proper error boundaries
- Write unit and integration tests for critical flows

## Frontend Responsibilities

### Pages
- `/auth/login` - User login page
- `/auth/register` - User registration page
- `/tasks` - Task management dashboard

### Components
- TaskForm - Create new tasks
- TaskDetail - View and edit tasks
- TaskActions - Delete and toggle completion
- ProtectedRoute - Authentication wrapper
- ErrorDisplay - Error messaging component

### Services
- API client with JWT attachment
- Authentication service
- Token management and refresh

## Testing Strategy

### Frontend Tests
- Unit tests for components
- Integration tests for API flows
- End-to-end tests for user flows
- Security tests for authentication

## Deployment

### Environment Variables
- NEXT_PUBLIC_API_BASE_URL - Backend API base URL
- NEXT_PUBLIC_BETTER_AUTH_URL - Better Auth configuration

### Build Process
- Use `npm run build` for production builds
- Optimize assets and bundle sizes
- Implement proper error pages