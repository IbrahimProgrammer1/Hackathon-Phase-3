-- Database Schema Migration: Initial Schema for Todo Application
-- Creates all required tables with proper relationships, indexes, and constraints

-- Enable UUID extension if not already enabled (for password reset tokens)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create credentials table
CREATE TABLE IF NOT EXISTS credentials (
    user_id VARCHAR(255) PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    name VARCHAR(255) NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    title TEXT NOT NULL CHECK (LENGTH(title) > 0),
    description TEXT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create password reset tokens table
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    token_hash TEXT NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance optimization
-- Index on tasks.user_id for optimizing user-based queries
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);

-- Index on tasks.completed for optimizing status-based queries
CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);

-- Index on users.email for optimizing email-based lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Index on password_reset_tokens.user_id for optimizing user-based queries
CREATE INDEX IF NOT EXISTS idx_password_reset_tokens_user_id ON password_reset_tokens(user_id);

-- Function to automatically update the updated_at column for tasks
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at column on tasks table
DROP TRIGGER IF EXISTS update_tasks_updated_at ON tasks;
CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE users IS 'Stores user account information';
COMMENT ON COLUMN users.user_id IS 'Unique identifier for the user';
COMMENT ON COLUMN users.email IS 'User email address';
COMMENT ON COLUMN users.created_at IS 'Timestamp when the user account was created';

COMMENT ON TABLE credentials IS 'Stores user credential information including password hashes';
COMMENT ON COLUMN credentials.user_id IS 'Reference to the user account';
COMMENT ON COLUMN credentials.name IS 'User display name';
COMMENT ON COLUMN credentials.password_hash IS 'BCrypt hash of the user password';
COMMENT ON COLUMN credentials.created_at IS 'Timestamp when the credentials were created';

COMMENT ON TABLE tasks IS 'Stores user tasks with completion status';
COMMENT ON COLUMN tasks.id IS 'Auto-incrementing primary key for tasks';
COMMENT ON COLUMN tasks.user_id IS 'Reference to the user who owns this task';
COMMENT ON COLUMN tasks.title IS 'Task title (required, non-empty)';
COMMENT ON COLUMN tasks.description IS 'Optional task description';
COMMENT ON COLUMN tasks.completed IS 'Boolean indicating if task is completed';
COMMENT ON COLUMN tasks.created_at IS 'Timestamp when the task was created';
COMMENT ON COLUMN tasks.updated_at IS 'Timestamp when the task was last updated';

COMMENT ON TABLE password_reset_tokens IS 'Stores password reset tokens with expiration';
COMMENT ON COLUMN password_reset_tokens.id IS 'UUID identifier for the reset token';
COMMENT ON COLUMN password_reset_tokens.user_id IS 'Reference to the user requesting reset';
COMMENT ON COLUMN password_reset_tokens.token_hash IS 'Hash of the reset token';
COMMENT ON COLUMN password_reset_tokens.expires_at IS 'Expiration timestamp for the token';
COMMENT ON COLUMN password_reset_tokens.used IS 'Flag indicating if token has been used';
COMMENT ON COLUMN password_reset_tokens.created_at IS 'Timestamp when the token was created';