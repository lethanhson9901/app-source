#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print step
print_step() {
    echo -e "${GREEN}==>${NC} $1"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}WARNING:${NC} $1"
}

# Function to print error and exit
print_error() {
    echo -e "${RED}ERROR:${NC} $1"
    exit 1
}

# Check Docker installation
if ! command_exists docker; then
    print_error "Docker is not installed. Please install Docker first."
fi

# Check Docker Compose installation
if ! command_exists docker-compose; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
fi

# Function to check docker service
check_docker_service() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker service is not running. Please start Docker service."
    fi
}

# Function to clean up
cleanup() {
    print_step "Cleaning up containers and volumes..."
    docker-compose down -v
    docker system prune -f
    print_step "Cleanup completed"
}

# Function to check service health
check_service_health() {
    local service=$1
    local max_attempts=30
    local attempt=1

    print_step "Waiting for $service to be healthy..."
    while [ $attempt -le $max_attempts ]; do
        if docker-compose ps | grep $service | grep -q "healthy"; then
            echo -e "${GREEN}$service is healthy${NC}"
            return 0
        fi
        echo "Attempt $attempt/$max_attempts: $service is not ready yet..."
        sleep 2
        ((attempt++))
    done
    print_error "$service failed to become healthy"
}

# Main execution
main() {
    # Check Docker service
    check_docker_service

    # Create necessary directories and files
    print_step "Setting up project structure..."
    chmod +x setup.sh
    ./setup.sh

    # Set environment
    print_step "Setting up environment..."
    if [ ! -f .env ]; then
        cp .env.development .env
        print_warning "Using development environment settings"
    fi

    # Build and start services
    print_step "Building and starting services..."
    docker-compose build --no-cache
    docker-compose up -d

    # Check services health
    check_service_health "postgres"
    check_service_health "redis"
    check_service_health "app"

    # Print access information
    print_step "Services are ready!"
    echo -e "${GREEN}Access the following services:${NC}"
    echo "- API: http://localhost:8080"
    echo "- API Documentation: http://localhost:8080/docs"
    echo "- Prometheus: http://localhost:8080/metrics"
    echo "- Grafana: http://localhost:8080/grafana (admin/admin)"

    # Print logs
    print_step "Showing logs (press Ctrl+C to exit)..."
    docker-compose logs -f
}

# Trap for cleanup
trap cleanup EXIT INT TERM

# Run main function
main
