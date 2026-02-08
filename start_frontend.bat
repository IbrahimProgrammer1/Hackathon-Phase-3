@echo off
echo Starting the frontend server...

REM Change to the frontend directory
cd frontend

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

REM Start the frontend development server
echo Starting the development server on http://localhost:3000
npm run dev