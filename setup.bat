@echo off
setlocal enabledelayedexpansion

echo ===========================================
echo Phase II Todo Full-Stack Application Setup
echo ===========================================

:: Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18.17+ or 20.6+
    exit /b 1
)

echo ✅ Node.js found

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.11+
    exit /b 1
)

echo ✅ Python found

:: Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip with Python
    exit /b 1
)

echo ✅ pip found

echo.
echo Installing backend dependencies...
cd backend

:: Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Upgrade pip
python -m pip install --upgrade pip

:: Install backend dependencies
pip install -r requirements.txt

echo.
echo Installing frontend dependencies...
cd ..\frontend

:: Install frontend dependencies
if exist "yarn.lock" (
    yarn install
) else (
    npm install
)

echo.
echo Setting up environment files...

:: Copy environment files if they don't exist
cd ..\backend
if not exist ".env" (
    copy .env.example .env
    echo Created backend/.env file - please update with your database and auth settings
)

cd ..\frontend
if not exist ".env.local" (
    copy .env.example .env.local
    echo Created frontend/.env.local file - please update with your API settings
)

echo.
echo ===========================================
echo Setup Complete!
echo ===========================================
echo.
echo To run the application:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   call venv\Scripts\activate.bat
echo   uvicorn main:app --reload --port 8000
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev  (or yarn dev)
echo.
echo The application will be available at:
echo   Frontend: http://localhost:3000
echo   Backend API: http://localhost:8000/api/docs
echo.
echo For production deployment, use Docker Compose:
echo   docker-compose up --build
echo.
pause