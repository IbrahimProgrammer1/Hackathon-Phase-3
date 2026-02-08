# Feature Specification: Phase II Todo Full-Stack Web App

**Feature Branch**: `001-todo-fullstack`
**Created**: 2026-01-06
**Status**: Draft
**Input**: User description (verbatim):

```text
Project: Phase II – Todo Full-Stack Web Application

Specification Scope:
This specification defines the functional, API, authentication, and persistence requirements
for transforming the Phase I Todo application into a secure, multi-user web application.

1. Core Features (Web)
- Task CRUD (Authenticated)
- All task operations scoped to authenticated user
- No cross-user access

2. Authentication & Authorization
- Better Auth (frontend)
- JWT in Authorization: Bearer <token>
- Backend verifies signature, extracts user identity; never trusts client user_id
- Missing/invalid JWT => 401; user mismatch/owner mismatch => 403

3. REST API
Base: /api/{user_id}
Endpoints:
- GET /tasks
- POST /tasks
- GET /tasks/{id}
- PUT /tasks/{id}
- DELETE /tasks/{id}
- PATCH /tasks/{id}/complete
Rules: valid JWT required; ownership enforced at query level; path user_id must match JWT user

4. Data Model & Persistence
- Neon Serverless PostgreSQL
- SQLModel ORM
- Task: id:int PK, user_id:str FK, title required, description optional, completed bool, created_at, updated_at
- User managed externally by Better Auth; identified by user_id string

5. Frontend
- Next.js 16+ App Router
- Handles signup/signin via Better Auth; manages JWT; attaches JWT to all backend API requests; renders responsive UI

6. NFRs
- Security: stateless JWT, expiry enforced
- Maintainability: monorepo separation
- Traceability: behavior traceable to spec; future changes require spec updates

Output expectations: sufficient to generate API contracts, DB schema, frontend integration; no implementation details; ambiguities deferred to /sp.clarify
```

## Clarifications

### Session 2026-01-06

- Q: For cross-user access to a task by ID, should the API return 403 or 404? → A: Return 404 Not Found (avoid leaking whether another user’s task ID exists).
- Q: What is the standardized error response shape? → A: JSON object: {"error": "Description of failure", "code": <HTTP status code>}.
- Q: What is the default authentication token lifetime? → A: 7 days.
- Q: How should invalid task ID formats be handled? → A: 400 Bad Request.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Manage my tasks securely (Priority: P1)

As a signed-in user, I want to create, view, update, complete, and delete my tasks so I can track my work from any device.

**Why this priority**: This is the core product value (task management) and must work end-to-end for a single user.

**Independent Test**: Sign in as a user, create a task, verify it appears in the task list, update it, toggle completion, then delete it; all actions succeed.

**Acceptance Scenarios**:

1. **Given** I am signed in, **When** I create a new task with a title, **Then** the task is saved and appears in my task list.
2. **Given** I have an existing task, **When** I edit its title and/or description, **Then** the changes are saved and shown when I view the task.
3. **Given** I have an existing task, **When** I mark it complete (or incomplete), **Then** the task status updates accordingly.
4. **Given** I have an existing task, **When** I delete it, **Then** it no longer appears in my task list.

---

### User Story 2 - My tasks are private by default (Priority: P2)

As a signed-in user, I want to be confident that I can only access my own tasks so that my task data remains private.

**Why this priority**: Multi-user privacy is the main difference from Phase I and is a hard security requirement.

**Independent Test**: Create tasks as User A; attempt to list/read/update/delete the same tasks as User B; User B is denied and cannot observe User A's tasks.

**Acceptance Scenarios**:

1. **Given** User A has tasks, **When** User B requests User A’s task list, **Then** access is denied.
2. **Given** User A owns a task, **When** User B attempts to fetch it by ID, **Then** the system responds "not found" and does not reveal whether such a task exists for any other user.
3. **Given** User A owns a task, **When** User B attempts to update/delete/complete it, **Then** the system responds "not found" and the task remains unchanged.

---

### User Story 3 - Clear sign-in requirement (Priority: P3)

As a visitor, I want to be prompted to sign in before using task features so that access to task data is protected.

**Why this priority**: Ensures the unauthenticated experience is consistent and enforces access boundaries.

**Independent Test**: While signed out, attempt to access task list or task details; the system blocks access and presents a sign-in path.

**Acceptance Scenarios**:

1. **Given** I am signed out, **When** I try to access task management features, **Then** I am required to sign in before viewing or changing tasks.

---

### Edge Cases

- Creating a task without a title is rejected with a clear, user-facing validation message.
- Requests made without valid authentication are rejected.
- Trying to access a task that does not exist returns a "not found" response without leaking whether another user owns a task with that ID.
- Concurrent updates: if a task is updated twice in quick succession, the final saved state matches the last confirmed update.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST require authentication before any task can be created, listed, retrieved, updated, completed, or deleted.
- **FR-002**: System MUST scope all task operations to the authenticated user; users MUST NOT be able to access or modify another user’s tasks.
- **FR-003**: System MUST support creating a task with a required title and an optional description.
- **FR-004**: System MUST allow an authenticated user to list all of their own tasks.
- **FR-005**: System MUST allow an authenticated user to retrieve a single task by its identifier, if it is owned by that user.
- **FR-006**: System MUST allow an authenticated user to update a task’s title and/or description, if it is owned by that user.
- **FR-007**: System MUST allow an authenticated user to delete a task, if it is owned by that user.
- **FR-008**: System MUST allow an authenticated user to mark a task complete or incomplete, if it is owned by that user.
- **FR-009**: System MUST reject requests that are missing authentication with an "Unauthorized" outcome.
- **FR-010**: System MUST reject requests where the authenticated identity does not match the requested user scope with a "Forbidden" outcome.
- **FR-011**: System MUST NOT rely solely on a user identifier provided by a client to determine resource ownership.
- **FR-012**: When a user attempts to retrieve/update/delete/complete a task by ID that is not owned by them, the system MUST respond with a "Not Found" outcome (to avoid leaking whether another user owns a task with that ID).
- **FR-013**: For any request that fails, the system MUST return a JSON error response shaped as: `{ "error": "Description of failure", "code": <HTTP status code> }`.
- **FR-014**: Authentication tokens MUST have a default lifetime of 7 days; requests using expired tokens MUST be rejected with an "Unauthorized" outcome.
- **FR-015**: Requests with an invalid task identifier format MUST be rejected with a "Bad Request" outcome.

### Key Entities *(include if feature involves data)*

- **User**: An authenticated account identified by a stable `user_id`.
- **Task**: A to-do item owned by exactly one user; attributes include an identifier, owner `user_id`, title, optional description, completion status, and created/updated timestamps.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A signed-in user can complete the full task lifecycle (create → view → update → complete → delete) with a success rate of 99% or higher over at least 50 repeated attempts.
- **SC-002**: While signed out, 100% of attempts to create/read/update/delete/complete tasks are blocked.
- **SC-003**: In cross-user tests (User B attempting to access User A’s tasks), 100% of attempts are blocked and User B cannot observe any of User A’s task data.
- **SC-004**: In user testing, at least 90% of users can create and complete a task without external assistance on their first attempt.
