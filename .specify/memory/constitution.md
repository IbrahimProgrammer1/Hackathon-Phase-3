<!--
Sync Impact Report:
- Version change: 2.1.0 → 3.0.0
- List of modified principles:
  - Added: I. AI-as-Interface (Interface layer only, no direct DB access)
  - Added: II. Tool-Based Execution (Deterministic and auditable AI actions)
  - Refined: III. Security & Ownership Identity (JWT as single source of truth, enforced for AI)
  - Refined: IV. Spec-Driven Development (Mandatory Spec-Kit Plus workflow)
  - Added: V. Progressive Evolution (Phase III builds on Phase II without breaking it)
  - Added: VI. Isolation of Concerns (Strict separation of AI, Backend, and Data layers)
- Added sections: System Architecture, Scope & Constraints
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->

# Todo Full-Stack (AI-Powered) Constitution

## Core Principles

### I. AI-as-Interface
AI is an interface layer, not an authority. It allows authenticated users to interact with tasks via natural language but must not directly access the database or bypass business logic. It operates strictly through defined tools.

### II. Tool-Based Execution
The AI agent must translate user intent into explicit, validated tool calls. It does not have free-form access to the backend. All operations must be deterministic, auditable, and mapped to existing API capabilities.

### III. Security & Ownership Identity
JWT remains the single source of truth for user identity. AI requests must include valid tokens. AI cannot fabricate access; cross-user attempts must return 404. AI tools enforce ownership identical to standard REST API requests.

### IV. Spec-Driven Development (SDD)
The project strictly follows the Spec-Kit Plus workflow: Constitution → Specify → Clarify → Plan → Tasks → Implement. No manual coding is permitted. AI behavior and tool contracts must be fully specified before implementation.

### V. Progressive Evolution
Phase III extends the application by introducing an AI layer without removing, rewriting, or weakening Phase I or Phase II milestones. Previous phase artifacts remain immutable and historically preserved.

### VI. Isolation of Concerns
Maintain strict separation between the AI reasoning layer, backend business logic, and data persistence layer. AI-related code is isolated in clearly defined directories to prevent cross-contamination with core services.

## System Architecture

### Technology Stack
- **Frontend**: Next.js 16+ (App Router) with an integrated authenticated chat UI.
- **Backend**: Python FastAPI with existing REST APIs and new AI tool endpoints.
- **AI Layer**: LLM-based conversational agent with a tool invocation framework; stateless execution per request.

### Authentication & Authorization
- Reuses Phase II JWT verification middleware.
- Backend derives user identity exclusively from JWT claims for all AI-initiated actions.
- AI cannot infer or assume permissions beyond those granted to the authenticated user.

## Scope & Constraints

### In-Scope (Phase III)
- Authenticated conversational interface for task interaction.
- Natural language support for CRUD operations (Create, List, Update, Delete).
- Translation of intent into validated tool calls.

### Non-Goals
- AI direct database access or bypass of auth/authz layers.
- Autonomous agent actions without explicit user intent.
- Introduction of new core task features beyond existing CRUD.

## Governance

### Amendment Procedure
The constitution supersedes all other practices. Any architectural or principle-level changes require a formal update to this document and a version increment.

### Versioning Policy
Semantic versioning is used:
- MAJOR: Backward incompatible governance or principle redefinitions (e.g., Phase III extension).
- MINOR: New principle or expanded guidance.
- PATCH: Clarifications and wording fixes.

### Compliance
All development tasks and code reviews must verify compliance with these principles. Complexity must be justified in implementation plans.

**Version**: 3.0.0 | **Ratified**: 2025-02-08 | **Last Amended**: 2026-02-08