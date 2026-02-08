# Production Setup Guide - Phase II Todo Full-Stack Application

## Project Overview

This is a secure, multi-user full-stack web application with persistent storage featuring:
- **Frontend**: Next.js 16+ with TypeScript, Tailwind CSS, Better Auth
- **Backend**: Python FastAPI with SQLModel, JWT authentication
- **Database**: PostgreSQL (Neon Serverless compatible)
- **Authentication**: JWT-based with 7-day token lifetime
- **Security**: Ownership enforcement, cross-user access prevention

## System Requirements

### Development Environment
- **Node.js**: 18.17+ or 20.6+ (LTS recommended)
- **Python**: 3.11+
- **npm/yarn**: Package manager for frontend dependencies
- **pip**: Package installer for Python
- **Git**: Version control system
- **OS**: Windows, macOS, or Linux

### Production Environment
- **Docker**: 20.10+ with Docker Compose
- **Memory**: 2GB RAM minimum (4GB recommended)
- **Storage**: 1GB available space
- **Ports**: 3000 (frontend), 8000 (backend), 5432 (database)

## Installation Methods

### Method 1: Automated Setup (Recommended)

#### On Windows:
```cmd
setup.bat
```

#### On macOS/Linux:
```bash
chmod +x setup.sh
./setup.sh
```

### Method 2: Manual Setup

#### Backend Setup:

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create Python virtual environment:**
```bash
python -m venv venv
```

3. **Activate virtual environment:**
- On Windows: `venv\Scripts\activate`
- On macOS/Linux: `source venv/bin/activate`

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your actual values
```

#### Frontend Setup:

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
# OR
yarn install
```

3. **Set up environment variables:**
```bash
cp .env.example .env.local
# Edit .env.local with your actual values
```

## Configuration

### Environment Variables

#### Backend (.env)
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db

# Authentication Secret (Generate a strong secret key)
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**Important Security Note**: Generate a strong random secret for `BETTER_AUTH_SECRET`. Use at least 32 characters of random data.

#### Frontend (.env.local)
```env
# Frontend Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000/auth
```

## Running the Application

### Development Mode

#### Backend:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

#### Frontend:
```bash
cd frontend
npm run dev  # OR yarn dev
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/docs (Swagger UI)

### Production Mode

#### Using Docker Compose (Recommended):
```bash
# Build and start containers
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

#### Direct Production Build:
```bash
# Backend
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Frontend (build first)
cd frontend
npm run build
npm start  # OR yarn start
```

## Security Configuration

### JWT Token Configuration
- **Lifetime**: 7 days (configurable)
- **Algorithm**: HS256
- **Secret**: Stored in `BETTER_AUTH_SECRET` environment variable
- **Verification**: Performed on every request requiring authentication

### Ownership Enforcement
- All API endpoints validate that `user_id` in JWT matches `user_id` in path
- Cross-user access attempts return HTTP 404 (not found) to prevent information leakage
- Database queries are filtered by authenticated user's `user_id`

### API Security
- All endpoints require JWT in `Authorization: Bearer <token>` header
- Standardized error responses: `{"error": "message", "code": status_code}`
- Input validation and sanitization on all endpoints

## Database Setup

### PostgreSQL Configuration
The application uses Neon Serverless PostgreSQL but is compatible with any PostgreSQL database.

#### Connection String Format:
```
postgresql://username:password@host:port/database_name
```

#### Required Extensions:
- `pgcrypto` (for encryption functions)

#### Schema Creation:
The application automatically creates required tables on startup via SQLModel.

## Testing

### Backend Tests:
```bash
cd backend
python -m pytest
```

### Frontend Tests:
```bash
cd frontend
npm run test  # OR yarn test
```

### End-to-End Tests:
```bash
# With both services running
npm run test:e2e  # OR yarn test:e2e
```

## Monitoring & Health Checks

### Health Endpoint:
- **Backend**: `GET /health` returns `{"status": "healthy", "service": "todo-api"}`

### API Documentation:
- **Backend**: `GET /api/docs` provides interactive Swagger UI
- **API Reference**: `GET /api/openapi.json` provides OpenAPI specification

## Deployment Strategies

### Docker Compose (Production Recommended)
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/todo_db
      - BETTER_AUTH_SECRET=your-secret-here
    depends_on:
      - db
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_BASE_URL=http://backend:8000/api
    depends_on:
      - backend
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: todo_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

### Environment-Specific Configurations

#### Staging Environment:
```bash
# Use different database and secret
DATABASE_URL=postgresql://staging-user:pass@staging-db:5432/todo_staging
BETTER_AUTH_SECRET=staging-secret-key
NEXT_PUBLIC_API_BASE_URL=https://staging-api.yourdomain.com/api
```

#### Production Environment:
```bash
# Use production database and strong secret
DATABASE_URL=postgresql://prod-user:pass@prod-db:5432/todo_prod
BETTER_AUTH_SECRET=$(openssl rand -hex 32)  # Generate secure random key
NEXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com/api
```

## Troubleshooting

### Common Issues:

1. **Port Already in Use**
   - Check if services are already running: `netstat -an | grep :8000` or `:3000`
   - Kill processes using the port if needed

2. **Database Connection Failed**
   - Verify `DATABASE_URL` is correct
   - Ensure PostgreSQL server is running
   - Check network connectivity to database

3. **Authentication Issues**
   - Verify `BETTER_AUTH_SECRET` matches between frontend and backend
   - Check JWT token format and expiration
   - Ensure `Authorization` header is sent with requests

4. **Environment Variables Not Loading**
   - Ensure .env files are properly named and located
   - Restart development servers after changing .env files
   - Check file permissions on .env files

### Debugging Tips:

- Enable verbose logging by setting environment variables
- Check application logs in console or log files
- Use browser developer tools to inspect API requests/responses
- Validate JWT tokens using online decoders

## Performance Optimization

### Backend Optimizations:
- Use connection pooling for database connections
- Implement caching for frequently accessed data
- Optimize database queries with proper indexing
- Use async/await for I/O operations

### Frontend Optimizations:
- Implement code splitting and lazy loading
- Use proper React.memo and useCallback hooks
- Optimize API calls with caching and debouncing
- Minimize bundle size with tree shaking

## Backup and Recovery

### Database Backup:
```bash
# Backup command
pg_dump -h hostname -U username -d database_name > backup.sql

# Restore command
psql -h hostname -U username -d database_name < backup.sql
```

### Configuration Backup:
- Backup all .env files separately (they contain secrets)
- Version control all configuration files except .env
- Document all environment-specific settings

## Maintenance Schedule

### Daily:
- Monitor application logs
- Check system resource usage
- Verify backup jobs completed successfully

### Weekly:
- Review security logs
- Update dependencies (test in staging first)
- Check for security patches

### Monthly:
- Performance review and optimization
- Database maintenance and optimization
- Security audit and penetration testing

## Final Verification Checklist

Before going live, ensure:

- [ ] All environment variables are properly configured
- [ ] Database connection is established and functional
- [ ] Authentication and authorization are working correctly
- [ ] API endpoints return proper responses
- [ ] Frontend communicates with backend successfully
- [ ] Security measures are in place and tested
- [ ] Error handling is graceful and informative
- [ ] Logging is configured and working
- [ ] Health checks pass successfully
- [ ] Load testing has been performed
- [ ] Backup procedures are tested and verified
- [ ] Monitoring and alerting are configured