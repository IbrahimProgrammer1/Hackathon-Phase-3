# Data Model: Phase II Todo Full-Stack Web App

## Entities

### Task
- **id** (Integer, Primary Key): Auto-incrementing unique identifier for the task
- **user_id** (String, Foreign Key): References the user who owns the task, matches the user_id from Better Auth
- **title** (String, Required): Task title with validation to ensure non-empty
- **description** (Text, Optional): Task description, can be empty
- **completed** (Boolean): Task completion status (true for complete, false for incomplete)
- **created_at** (Timestamp): Timestamp when the task was created
- **updated_at** (Timestamp): Timestamp when the task was last updated

### User
- **user_id** (String, Primary Key): Unique identifier provided by Better Auth, stored as the foreign key in tasks
- **email** (String, Optional): User's email address from Better Auth (for potential future use)
- **created_at** (Timestamp): When the user account was created (via Better Auth)

## Relationships
- Task belongs to User (many-to-one): Each task is owned by exactly one user via the user_id foreign key
- User has many Tasks: A user can have multiple tasks associated with their account

## Validation Rules
- Task title must be non-empty
- Task title and description must be properly escaped to prevent injection
- User_id must match the authenticated user's ID for any task operations
- Task completion status can only be toggled by the task owner

## State Transitions
- Task starts as 'incomplete' when created
- Task can transition to 'complete' when marked as done
- Task can transition back to 'incomplete' if unmarked
- Task is removed from the user's view when deleted (but may remain in database for audit purposes)