<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0 (MINOR - new principles and sections added)
- Modified principles: Added Deliverable Focus (VI) and Functional Completeness (VII)
- Added sections: Project Overview, Constraints, Stakeholders
- Templates requiring updates: ✅ All checked (plan-template.md, spec-template.md, tasks-template.md)
- No files flagged for manual follow-up
- No placeholders deferred
-->

# Phase I - Todo In-Memory Python Console App Constitution

## Project Overview

**Title**: Phase I - Todo In-Memory Python Console App
**Objective**: Build a command-line todo application that stores tasks in memory.
**Scope**:
- Implement basic todo functionality: Add, Delete, Update, View, Mark Complete
- Store tasks in memory only (no database)
- Use Python 3.13+, Claude Code, and Spec-Kit Plus
- Follow clean code principles and proper Python project structure

## Core Principles

### I. SDD (Spec-Driven Development) Mandatory
Every implementation step must follow the Spec -> Plan -> Tasks workflow. No code is written without prior architectural alignment.

### II. In-Memory Simplicity
For Phase I, no persistent storage (database/files) is allowed. All state must be managed in-memory, emphasizing clean data structures.

### III. Pythonic Excellence
Follow PEP 8, use strong typing with Python 3.13 features, and maintain modular code within the `src/` directory.

### IV. CLI First
The interface is strictly command-line based. Commands (`add-task`, `list-tasks`, `update-task`, `delete-task`, `complete-task`) must be intuitive and follow standard CLI patterns.

### V. Testable by Design
Features must be architected for easy verification via automated tests or clear CLI outputs.

### VI. Deliverable Focus
The project must deliver a GitHub repository containing:
- Constitution file
- Specs history folder with phase-specific specs
- `/src` folder with Python source code
- README.md with setup instructions
- CLAUDE.md with Claude Code instructions

### VII. Functional Completeness
The working console application must demonstrate:
- Adding tasks with title and description
- Listing all tasks with status indicators
- Updating task details
- Deleting tasks by ID
- Marking tasks as complete/incomplete

## Technology Stack
- **Language**: Python 3.13+
- **Dev Tools**: Claude Code, Spec-Kit Plus
- **Environment**: win32

## Development Workflow
1. /sp.specify -> Define requirements.
2. /sp.plan -> Architect the solution.
3. /sp.tasks -> Break down into actionable steps.
4. /sp.implement -> Execute the build.

## Constraints
- CLI commands should be descriptive: `add-task`, `delete-task`, `update-task`, `list-tasks`, `complete-task`
- No persistent storage required
- All development must use Spec-Kit Plus and Claude Code (no manual coding)

## Stakeholders
- Hackathon Reviewers (GIAIC)
- Developer Team (Yourself)

## Governance
This constitution supersedes ad-hoc decisions. Changes require re-ratification.

**Version**: 1.1.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
