# Neon DB API Key Rotation & Schema Setup

This document outlines the changes made during the Neon DB API key rotation and database schema setup.

## Configuration Updates

### 1. Environment Variables Updated

The following files had their database configuration updated:

- `.env.local` - Updated with the new Neon DB API key
- `.env.example` - Template updated with proper format

### 2. Database URL Format Correction

The original `.env.local` file had incorrect formatting with `psql` prefix and unnecessary quotes. The corrected format is:

```
DATABASE_URL=postgresql://neondb_owner:npg_fhG2yEPe5pDi@ep-billowing-bread-aixdccti-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

## Database Schema

### Tables Created

Based on the SQLModel definitions in the application, the following tables were created:

1. **users** - Stores user account information
2. **credentials** - Stores user credential information including password hashes
3. **tasks** - Stores user tasks with completion status
4. **password_reset_tokens** - Stores password reset tokens with expiration

### Indexes Created

- `idx_tasks_user_id` - Index on tasks.user_id for optimizing user-based queries
- `idx_tasks_completed` - Index on tasks.completed for optimizing status-based queries
- `idx_users_email` - Index on users.email for optimizing email-based lookups
- `idx_password_reset_tokens_user_id` - Index on password_reset_tokens.user_id

## Migration Scripts

Two scripts were created to manage the database:

1. `backend/migrations/001_create_initial_schema.sql` - SQL script to create all tables and indexes
2. `backend/scripts/db_migrate.py` - Python script to run the migration process
3. `backend/scripts/db_verify.py` - Python script to verify database connectivity and schema

## Migration Process

1. Test database connection with new API key
2. Execute SQL migration script to create tables and indexes
3. Create additional indexes using application logic
4. Verify all required tables exist
5. Test basic CRUD operations

## Security Considerations

- All passwords are stored as bcrypt hashes
- Password reset tokens are stored as hashed values
- SSL mode is required for all PostgreSQL connections
- User isolation is enforced through user_id foreign keys
- JWT authentication is used for all API operations