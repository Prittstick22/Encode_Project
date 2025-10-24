#!/bin/bash

# Portfolio Management Application Setup Script

set -e

echo "========================================="
echo "Portfolio Management Application Setup"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env file to add your OpenAI API key if needed."
fi

# Build and start services
echo ""
echo "Building and starting services..."
docker-compose up -d --build

# Wait for services to be healthy
echo ""
echo "Waiting for services to be ready..."
sleep 10

# Check service status
echo ""
echo "Checking service status..."
docker-compose ps

# Print access information
echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Services are now running:"
echo "  - Backend API: http://localhost:5000"
echo "  - Grafana Dashboard: http://localhost:3000 (admin/admin)"
echo "  - Prometheus: http://localhost:9090"
echo "  - PostgreSQL: localhost:5432"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop services:"
echo "  docker-compose down"
echo ""
echo "Next steps:"
echo "  1. Open Grafana at http://localhost:3000"
echo "  2. Login with admin/admin"
echo "  3. Navigate to Dashboards → Portfolio Management Dashboard"
echo "  4. Create a portfolio using the API"
echo ""
echo "Example API call to create a portfolio:"
echo "  curl -X POST http://localhost:5000/api/portfolios \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"name\": \"My Portfolio\", \"user_type\": \"retail_investor\"}'"
echo ""
