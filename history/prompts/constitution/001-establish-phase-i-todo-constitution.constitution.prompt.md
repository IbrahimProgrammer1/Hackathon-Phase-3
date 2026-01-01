---
id: 1
title: Establish Phase I Todo Constitution
stage: constitution
date: 2026-01-01
surface: agent
model: claude-opus-4.5
feature: none
branch: master
user: default
command: /sp.constitution
labels: [constitution, setup, phase-i]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution

Title: Phase I - Todo In-Memory Python Console App
Objective: Build a command-line todo application that stores tasks in memory.
Scope:
  - Implement basic todo functionality: Add, Delete, Update, View, Mark Complete
  - Store tasks in memory only (no database)
  - Use Python 3.13+, Claude Code, and Spec-Kit Plus
  - Follow clean code principles and proper Python project structure
Deliverables:
  - GitHub repository containing:
      * Constitution file
      * specs history folder with phase-specific specs
      * /src folder with Python source code
      * README.md with setup instructions
      * CLAUDE.md with Claude Code instructions
  - Working console application demonstrating:
      * Adding tasks with title and description
      * Listing all tasks with status indicators
      * Updating task details
      * Deleting tasks by ID
      * Marking tasks as complete/incomplete
Constraints:
  - CLI commands should be descriptive:
      * add-task
      * delete-task
      * update-task
      * list-tasks
      * complete-task
  - No persistent storage required
  - All development must use Spec-Kit Plus and Claude Code (no manual coding)
Stakeholders:
  - Hackathon Reviewers (GIAIC)
  - Developer Team (Yourself)

## Response snapshot

Established the Phase I Todo In-Memory Python Console App Constitution at `.specify/memory/constitution.md`.

## Outcome

- ✅ Impact: Project principles and success criteria defined.
- 🧪 Tests: N/A
- 📁 Files: Created `.specify/memory/constitution.md`.
- 🔁 Next prompts: /sp.specify for initial requirements.
- 🧠 Reflection: Constitution aligns with SDD and provides clear guardrails for Phase I.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
