@echo off
echo Starting the backend server...

REM Change to the backend directory
cd backend

REM Check if virtual environment exists, if not create it
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Start the backend server
echo Starting the server on http://localhost:8000
uvicorn main:app --host 0.0.0.0 --port 8000 --reload