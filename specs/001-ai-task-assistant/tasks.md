# Tasks: AI-Powered Task Assistant

**Input**: Design documents from `/specs/001-ai-task-assistant/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/ai_tools.md, research.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup

**Purpose**: Project initialization and basic structure for AI features.

- [ ] T001 Create backend AI structure in `backend/src/api/ai_agent.py`, `backend/src/services/ai_service.py`, and `backend/src/models/ai_tools.py`
- [ ] T002 [P] Configure environment variables for `OPENAI_API_KEY` and `AI_MODEL` in `backend/.env`
- [ ] T003 Create frontend chat structure in `frontend/src/components/chat/`, `frontend/src/services/ai_api.ts`, and `frontend/src/contexts/ChatContext.tsx`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for intent parsing and tool execution.

- [ ] T004 Implement Pydantic models for AI tools in `backend/src/models/ai_tools.py` per `contracts/ai_tools.md`
- [ ] T005 Setup OpenAI client and base intent parsing service in `backend/src/services/ai_service.py`
- [ ] T006 Implement AI chat endpoint in `backend/src/api/ai_agent.py` with existing JWT middleware protection
- [ ] T007 Implement `user_id` extraction from JWT in `backend/src/api/ai_agent.py` to ensure ownership enforcement

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1)

**Goal**: Allow users to create tasks via chat messages.

**Independent Test**: Send "Remind me to buy milk" in chat and verify a task "buy milk" is created in the user's task list.

- [ ] T008 [US1] Implement `create_task` tool logic in `backend/src/services/ai_service.py` mapping to `TaskService.create_task`
- [ ] T009 [US1] Create basic chat interface component in `frontend/src/components/chat/ChatWidget.tsx`
- [ ] T010 [US1] Implement frontend API service in `frontend/src/services/ai_api.ts` to call `/api/v1/ai/chat`
- [ ] T011 [US1] Connect `ChatWidget` to `ChatContext` and `ai_api.ts` to send and display messages

---

## Phase 4: User Story 2 - Task Listing and Querying (Priority: P1)

**Goal**: Allow users to list and query tasks via chat.

**Independent Test**: Ask "What are my tasks?" and verify the assistant returns the list of current incomplete tasks.

- [ ] T012 [US2] Implement `list_tasks` tool logic in `backend/src/services/ai_service.py` mapping to `TaskService.get_user_tasks`
- [ ] T013 [US2] Enhance AI response formatting in `backend/src/services/ai_service.py` to display task lists clearly
- [ ] T014 [US2] [P] Update `ChatWidget.tsx` to handle and display structured task lists returned by the AI

---

## Phase 5: User Story 3 - Safe Task Deletion (Priority: P2)

**Goal**: Allow users to delete tasks conversationally with explicit confirmation by title.

**Independent Test**: Send "Delete my last task", verify AI asks "Are you sure you want to delete '[Title]'?", confirm "Yes", and verify task is gone.

- [ ] T015 [US3] Implement relative reference resolution (e.g., "last task") in `backend/src/services/ai_service.py`
- [ ] T016 [US3] Implement `delete_task` tool logic with confirmation requirement in `backend/src/services/ai_service.py`
- [ ] T017 [US3] Update `backend/src/api/ai_agent.py` to handle confirmation-required tool flow (State Transition: Ask Confirmation)
- [ ] T018 [US3] Implement confirmation UI in `frontend/src/components/chat/ChatWidget.tsx`

---

## Phase 6: User Story 4 - Intent and Entity Clarification (Priority: P2)

**Goal**: Handle ambiguous requests or multiple task matches.

**Independent Test**: Send "Delete milk" when two milk tasks exist, and verify AI asks which one to delete.

- [ ] T019 [US4] Implement `update_task` and `toggle_task_completion` tools in `backend/src/services/ai_service.py`
- [ ] T020 [US4] Implement multi-match detection logic in `backend/src/services/ai_service.py` for ambiguous titles
- [ ] T021 [US4] Add "Clarification" state to AI service to present options to the user per FR-011

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Security, performance, and error handling.

- [ ] T022 Implement 10-message sliding window context in `frontend/src/contexts/ChatContext.tsx` per FR-009
- [ ] T023 Add strict system instructions and safety guardrails in `backend/src/services/ai_service.py` to prevent prompt injection per FR-012
- [ ] T024 Implement differentiated error handling (Conversational Validation vs. Generic System) in `backend/src/api/ai_agent.py` per FR-010
- [ ] T025 [P] Final UI styling for `ChatWidget.tsx` using Tailwind CSS to match Phase II design

---

## Dependencies & Execution Order

1. **Setup (Phase 1)** -> **Foundational (Phase 2)**: Core structure and tool base must exist.
2. **Foundational (Phase 2)** -> **US1 (Phase 3)**: Creation is the simplest first feature.
3. **US1 (Phase 3)** -> **US2 (Phase 4)**: Listing depends on having creation working for easy testing.
4. **US1/US2** -> **US3/US4 (Phase 5/6)**: Advanced conversational flows depend on basic CRUD tools.
5. **All Stories** -> **Polish (Phase 7)**: Final hardening and UX improvements.

## Implementation Strategy

- **MVP First**: Complete Phase 1, 2, and 3 to have a working "Add task via chat" feature.
- **Incremental Delivery**: Add Listing (US2), then Deletion (US3) with confirmation, then Clarification (US4).
- **Security Check**: Verify JWT ownership enforcement (T007) is working before any write operations are enabled.
