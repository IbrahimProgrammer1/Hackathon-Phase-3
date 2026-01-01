---
description: "Task list for Phase I - Todo In-Memory Python Console App implementation"
---

# Tasks: Phase I - Todo In-Memory Python Console App

**Input**: Design documents from `/specs/todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 [P] Create project structure per implementation plan: `src/`, `src/models/`, `src/services/`, `src/cli/`, `src/utils/`
- [ ] T002 [P] Initialize Git repository and create initial commit
- [ ] T003 [P] Create README.md with setup instructions
- [ ] T004 [P] Create CLAUDE.md with Claude Code instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create Task class with fields: id (auto-increment integer), title, description, status in `src/models/task.py`
- [ ] T006 Implement Task validation: ensure title/description are non-empty in `src/models/task.py`
- [ ] T007 Create TaskManager service for in-memory storage in `src/services/task_manager.py`
- [ ] T008 Create CLI argument parser in `src/cli/commands.py`
- [ ] T009 Set up main application entry point in `src/main.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and List Tasks (Priority: P1) 🎯 MVP

**Goal**: Core functionality to add tasks and list them with status indicators

**Independent Test**: Can be fully tested by adding tasks and listing them to verify they appear correctly with status indicators.

### Implementation for User Story 1

- [ ] T010 [P] [US1] Implement add-task command in `src/cli/commands.py` with input validation
- [ ] T011 [P] [US1] Implement add_task method in TaskManager service in `src/services/task_manager.py`
- [ ] T012 [US1] Implement list-tasks command in `src/cli/commands.py` to display all tasks
- [ ] T013 [US1] Implement get_all_tasks method in TaskManager service in `src/services/task_manager.py`
- [ ] T014 [US1] Add status indicators (✅ for complete, ⬜ for incomplete) when listing tasks
- [ ] T015 [US1] Add confirmation message for add-task command

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Update and Delete Tasks (Priority: P2)

**Goal**: Functionality to update or delete existing tasks

**Independent Test**: Can be tested by adding a task, updating its details or deleting it, and then listing tasks to verify the change.

### Implementation for User Story 2

- [ ] T016 [P] [US2] Implement update-task command in `src/cli/commands.py` with partial update support
- [ ] T017 [P] [US2] Implement update_task method in TaskManager service in `src/services/task_manager.py`
- [ ] T018 [US2] Implement delete-task command in `src/cli/commands.py`
- [ ] T019 [US2] Implement delete_task method in TaskManager service in `src/services/task_manager.py`
- [ ] T020 [US2] Add confirmation messages for update and delete actions

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Tasks Complete (Priority: P3)

**Goal**: Functionality to mark tasks as complete or incomplete

**Independent Test**: Can be tested by adding a task, marking it as complete, and then listing tasks to verify the status indicator changes.

### Implementation for User Story 3

- [ ] T021 [US3] Implement complete-task command in `src/cli/commands.py` with toggle functionality
- [ ] T022 [US3] Implement toggle_task_status method in TaskManager service in `src/services/task_manager.py`
- [ ] T023 [US3] Add confirmation messages for complete-task action

**Checkpoint**: All core functionality should now be independently functional

---

## Phase 6: User Story 4 - Input Validation and Error Handling (Priority: P4)

**Goal**: Robust validation and error handling for all inputs

**Independent Test**: Can be tested by providing invalid inputs and verifying appropriate error messages are displayed.

### Implementation for User Story 4

- [ ] T024 [P] [US4] Create input validation utilities in `src/utils/validation.py`
- [ ] T025 [P] [US4] Implement whitespace trimming for user inputs
- [ ] T026 [US4] Implement numeric ID string conversion to integers
- [ ] T027 [US4] Add error handling for invalid IDs with "Error:" prefix
- [ ] T028 [US4] Ensure app continues running after errors (not exit)
- [ ] T029 [US4] Add error handling for empty title/description in update-task

**Checkpoint**: All user stories should now have proper validation and error handling

---

## Phase 7: Polish & User Experience

**Purpose**: Enhancements to improve user experience

- [ ] T030 [P] Implement quit/exit commands for graceful termination in `src/cli/commands.py`
- [ ] T031 [P] Add graceful exit message when exiting the application
- [ ] T032 [P] Ensure tasks display in insertion order as required
- [ ] T033 [P] Add support for special characters in titles and descriptions
- [ ] T034 [P] Update README.md with usage instructions for all commands
- [ ] T035 [P] Run comprehensive testing to verify all functionality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence