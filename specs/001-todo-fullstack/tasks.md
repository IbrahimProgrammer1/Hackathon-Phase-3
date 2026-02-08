# Tasks: Phase II Todo Full-Stack Web Application

**Feature**: Phase II Todo Full-Stack Web Application
**Branch**: 001-todo-fullstack
**Input**: spec.md, plan.md, data-model.md, contracts/

## Phase 1: Project Setup

### Setup Tasks

- [X] T001 Create feature branch 001-todo-fullstack
- [X] T002 [P] Initialize frontend Next.js app with TypeScript + Tailwind in frontend/ directory
- [X] T003 [P] Initialize backend FastAPI app with SQLModel in backend/ directory
- [X] T004 [P] Update root CLAUDE.md with new technology stack (Next.js, FastAPI, SQLModel, Better Auth)
- [X] T005 [P] Create initial directory structure in backend/src/models, backend/src/services, backend/src/api, frontend/src/components, frontend/src/pages

## Phase 2: Foundational Components

### Database Setup

- [X] T006 Define SQLModel models for User and Task in backend/src/models/task_model.py
- [X] T007 Configure Neon PostgreSQL connection in backend/src/database.py
- [X] T008 Create environment variable setup with BETTER_AUTH_SECRET and DATABASE_URL
- [X] T009 Add indexes for tasks.user_id and tasks.completed in database schema

### Authentication Infrastructure

- [X] T010 [P] Implement JWT verification middleware in backend/src/middleware/auth.py
- [X] T011 [P] Create Better Auth integration in frontend/src/lib/auth.ts
- [X] T012 [P] Implement API client with JWT attachment in frontend/src/lib/api.ts

## Phase 3: User Story 1 - Manage my tasks securely (Priority: P1)

**Goal**: As a signed-in user, I want to create, view, update, complete, and delete my tasks so I can track my work from any device.

**Independent Test**: Sign in as a user, create a task, verify it appears in the task list, update it, toggle completion, then delete it; all actions succeed.

### Backend API Implementation

- [X] T013 [US1] Implement GET /api/{user_id}/tasks endpoint with JWT ownership enforcement in backend/src/api/tasks.py
- [X] T014 [US1] Implement POST /api/{user_id}/tasks endpoint for creating tasks with JWT verification in backend/src/api/tasks.py
- [X] T015 [US1] Implement GET /api/{user_id}/tasks/{id} endpoint for task detail with ownership check in backend/src/api/tasks.py
- [X] T016 [US1] Implement PUT /api/{user_id}/tasks/{id} endpoint for updating tasks with ownership check in backend/src/api/tasks.py
- [X] T017 [US1] Implement DELETE /api/{user_id}/tasks/{id} endpoint with ownership enforcement in backend/src/api/tasks.py
- [X] T018 [US1] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint for toggling completion status in backend/src/api/tasks.py
- [X] T019 [US1] Standardize error responses (400, 401, 403, 404) with consistent JSON format in backend/src/api/error_handlers.py

### Frontend Implementation

- [X] T020 [US1] Create task list page to display authenticated user's tasks in frontend/src/app/tasks/page.tsx
- [X] T021 [US1] Create task creation form component in frontend/src/components/TaskForm.tsx
- [X] T022 [US1] Create task detail/update component in frontend/src/components/TaskDetail.tsx
- [X] T023 [US1] Implement task deletion functionality in frontend/src/components/TaskActions.tsx
- [X] T024 [US1] Implement task completion toggle functionality in frontend/src/components/TaskActions.tsx
- [X] T025 [US1] Integrate API client with task operations in frontend/src/services/taskService.ts

## Phase 4: User Story 2 - My tasks are private by default (Priority: P2)

**Goal**: As a signed-in user, I want to be confident that I can only access my own tasks so that my task data remains private.

**Independent Test**: Create tasks as User A; attempt to list/read/update/delete the same tasks as User B; User B is denied and cannot observe User A's tasks.

### Backend Security Implementation

- [X] T026 [US2] Enhance ownership enforcement in all task endpoints to return 404 for cross-user access attempts
- [X] T027 [US2] Add validation to ensure path user_id matches JWT user_id in backend/src/api/tasks.py
- [X] T028 [US2] Implement proper error handling for invalid task ID formats (400 Bad Request)

### Frontend Security Implementation

- [X] T029 [US2] Update frontend to handle 404 responses appropriately for cross-user access attempts
- [X] T030 [US2] Implement proper error display for security-related responses in frontend/src/components/ErrorDisplay.tsx

## Phase 5: User Story 3 - Clear sign-in requirement (Priority: P3)

**Goal**: As a visitor, I want to be prompted to sign in before using task features so that access to task data is protected.

**Independent Test**: While signed out, attempt to access task list or task details; the system blocks access and presents a sign-in path.

### Authentication Implementation

- [X] T031 [US3] Implement Better Auth signup/login pages in frontend/src/app/auth/
- [X] T032 [US3] Create protected route wrapper in frontend/src/components/ProtectedRoute.tsx
- [X] T033 [US3] Implement JWT storage and retrieval in frontend/src/lib/authStorage.ts
- [X] T034 [US3] Handle expired token scenarios (7-day lifetime) in frontend/src/lib/auth.ts
- [X] T035 [US3] Redirect unauthenticated users to sign-in page when accessing protected features

## Phase 6: Testing & Verification

### Backend Testing

- [X] T036 Create backend unit tests for CRUD operations in backend/tests/test_tasks.py
- [X] T037 Create backend unit tests for JWT verification in backend/tests/test_auth.py
- [X] T038 Create backend unit tests for ownership enforcement in backend/tests/test_authz.py

### Frontend Testing

- [X] T039 Create frontend integration tests for auth flow in frontend/tests/auth.test.tsx
- [X] T040 Create frontend integration tests for task actions in frontend/tests/tasks.test.tsx
- [X] T041 Create frontend tests for error handling scenarios in frontend/tests/errors.test.tsx

### End-to-End Testing

- [X] T042 Create end-to-end user scenario tests in tests/e2e/user_flow.test.ts

## Phase 7: Documentation & Polish

### Documentation Updates

- [X] T043 Update frontend CLAUDE.md with frontend-specific instructions
- [X] T044 Update backend CLAUDE.md with backend-specific instructions
- [X] T045 Ensure spec references are up to date in all documentation
- [X] T046 Update README.md with setup instructions for full-stack application

### Final Integration & Polish

- [X] T047 Integrate frontend and backend for complete user flow
- [X] T048 Perform end-to-end testing of all user stories
- [X] T049 Fix any integration issues discovered during testing
- [X] T050 Deploy to test environment for validation

## Dependencies

### User Story Completion Order
1. User Story 1 (Core task management) must be completed before User Story 2 (Privacy) and User Story 3 (Auth requirement)
2. User Story 2 and User Story 3 can be developed in parallel after User Story 1 foundation is complete

### Task Dependencies
- T002, T003 depend on T001 (Project setup)
- T006-T009 depend on T003 (Database setup after backend init)
- T013-T019 depend on T006-T009 (API endpoints after DB models)
- T020-T025 depend on T013-T019 and T011-T012 (Frontend after backend API and auth)
- T026-T030 depend on T013-T019 (Security enhancements after basic API)
- T031-T035 depend on T011 (Auth pages after auth integration)
- T036-T042 depend on T013-T035 (Tests after implementation)

## Parallel Execution Examples

### Within User Story 1
- T013 (GET tasks) and T014 (POST task) can be developed in parallel [P]
- T020 (task list page) and T021 (task form) can be developed in parallel [P]
- T023 (task deletion) and T024 (task completion) can be developed in parallel [P]

### Across User Stories
- T026-T030 (User Story 2 security) can be developed in parallel with T031-T035 (User Story 3 auth) after T025 is complete

## Implementation Strategy

### MVP Scope (Minimum Viable Product)
1. Complete Phase 1 (Project setup)
2. Complete Phase 2 (Foundational components)
3. Complete User Story 1 (Core task management) - T013 through T025
4. This provides a working application where a user can sign in and manage their tasks

### Incremental Delivery
1. MVP: User Story 1 (Core task management)
2. Security: User Story 2 (Privacy enforcement)
3. Access control: User Story 3 (Sign-in requirement)
4. Quality: Testing & Documentation