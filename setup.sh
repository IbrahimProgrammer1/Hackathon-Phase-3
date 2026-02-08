#!/bin/bash

# Phase II Todo Full-Stack Application Setup Script
set -e  # Exit on any error

echo "==========================================="
echo "Phase II Todo Full-Stack Application Setup"
echo "==========================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18.17+ or 20.6+"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2)
NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)

if [ "$NODE_MAJOR" -lt 18 ]; then
    echo "❌ Node.js version $NODE_VERSION is too old. Please install Node.js 18.17+ or 20.6+"
    exit 1
fi

echo "✅ Node.js version $NODE_VERSION found"

# Check if Python is installed
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.11+"
    exit 1
fi

PYTHON_CMD=python
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
fi

PYTHON_VERSION=$($PYTHON_CMD --version | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
    echo "❌ Python version $PYTHON_VERSION is too old. Please install Python 3.11+"
    exit 1
fi

echo "✅ Python version $PYTHON_VERSION found"

# Check if pip is available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip with Python"
    exit 1
fi

echo ""
echo "Installing backend dependencies..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Unix/Linux/macOS
    source venv/bin/activate
fi

# Upgrade pip
pip install --upgrade pip

# Install backend dependencies
pip install -r requirements.txt

echo ""
echo "Installing frontend dependencies..."
cd ../frontend

# Install frontend dependencies
if command -v yarn &> /dev/null; then
    yarn install
elif command -v npm &> /dev/null; then
    npm install
else
    echo "❌ Neither npm nor yarn found. Please install Node.js with npm."
    exit 1
fi

echo ""
echo "Setting up environment files..."

# Copy environment files if they don't exist
cd ../backend
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created backend/.env file - please update with your database and auth settings"
fi

cd ../frontend
if [ ! -f ".env.local" ]; then
    cp .env.example .env.local
    echo "Created frontend/.env.local file - please update with your API settings"
fi

echo ""
echo "==========================================="
echo "Setup Complete!"
echo "==========================================="
echo ""
echo "To run the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "  uvicorn main:app --reload --port 8000"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev  # or yarn dev"
echo ""
echo "The application will be available at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000/api/docs"
echo ""
echo "For production deployment, use Docker Compose:"
echo "  docker-compose up --build"
echo ""