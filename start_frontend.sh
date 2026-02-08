#!/bin/bash
# Script to start the frontend development server

echo "Starting the frontend server..."

# Change to the frontend directory
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start the frontend development server
echo "Starting the development server on http://localhost:3000"
npm run dev