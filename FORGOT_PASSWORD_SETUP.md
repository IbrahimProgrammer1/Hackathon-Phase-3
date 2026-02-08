# Forgot Password Feature Setup Guide

## Overview
The forgot password feature has been successfully implemented in your TODO app. This guide explains how to set up and use the feature.

## Prerequisites
- Backend server running on `http://localhost:8000`
- Frontend server running on `http://localhost:3000`
- Database properly configured

## Setting Up the Servers

### 1. Backend Server Setup
```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment (if not already created)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend Server Setup
```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

## Using the Forgot Password Feature

1. Go to the login page (`http://localhost:3000/auth/login`)
2. Click on "Forgot password?" link
3. Enter your registered email address
4. Submit the form

## How It Works

### Backend Endpoints
- `POST /api/auth/forgot-password` - Requests password reset
- `POST /api/auth/validate-reset-token` - Validates reset token
- `POST /api/auth/reset-password` - Resets the password

### Database Table
The system creates a `password_reset_tokens` table to securely store reset tokens with:
- Unique token identifier
- Associated user ID
- Token hash (for security)
- Expiration timestamp
- Usage status

## Troubleshooting

### "Not Found" Error
If you're getting a "Not Found" error when submitting the email:

1. **Check if backend server is running**: Ensure the backend server is running on `http://localhost:8000`
2. **Verify API endpoint**: The frontend calls `/api/auth/forgot-password` which maps to `http://localhost:8000/api/auth/forgot-password`
3. **Check environment variables**: Make sure `NEXT_PUBLIC_API_BASE_URL` in your frontend `.env.local` file is set to `http://localhost:8000`

### Sample .env.local file for frontend:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Sample .env file for backend:
```
DATABASE_URL=sqlite:///./todo_dev.db
BETTER_AUTH_SECRET=your-super-secret-key-change-this-in-production
APP_URL=http://localhost:3000
```

## Security Features
- Reset tokens are securely generated using `secrets.token_urlsafe(32)`
- Tokens are hashed before storage for security
- Tokens expire after 1 hour
- Tokens can only be used once
- Email enumeration is prevented (same response regardless of email existence)

## Testing the Feature
1. Register a user account with a test email
2. Go to the forgot password page
3. Enter the registered email
4. Check the server console for the reset link (since email sending is mocked)
5. Copy the reset link and paste it in your browser
6. Enter a new password and confirm it
7. Try logging in with the new password

The feature is now fully functional and secure!