#!/bin/bash
# Script to start the backend server

echo "Starting the backend server..."

# Change to the backend directory
cd backend

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the backend server
echo "Starting the server on http://localhost:8000"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload