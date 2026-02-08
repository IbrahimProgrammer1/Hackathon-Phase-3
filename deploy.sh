#!/bin/bash

# Production Deployment Script for Phase II Todo Full-Stack Application

set -e  # Exit on any error

echo "==========================================="
echo "Production Deployment Script"
echo "Phase II Todo Full-Stack Application"
echo "==========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop or Docker Engine."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker and Docker Compose found"

# Build and deploy the application
echo ""
echo "Building and deploying the application..."
docker-compose up --build -d

echo ""
echo "Waiting for services to start..."
sleep 10

# Check if services are running
echo ""
echo "Checking service status..."
docker-compose ps

echo ""
echo "==========================================="
echo "Deployment Complete!"
echo "==========================================="
echo ""
echo "Services are now running:"
echo "  Frontend: http://localhost:3000"
echo "  Backend: http://localhost:8000"
echo "  Database: localhost:5432 (PostgreSQL)"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop the application:"
echo "  docker-compose down"
echo ""
echo "To rebuild and restart:"
echo "  docker-compose down && docker-compose up --build -d"
echo ""