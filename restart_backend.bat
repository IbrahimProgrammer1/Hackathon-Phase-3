@echo off
echo Stopping all Python/Uvicorn processes...
taskkill /F /IM python.exe /T
timeout /t 2
echo Starting backend server...
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
