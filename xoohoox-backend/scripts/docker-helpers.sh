#!/bin/bash

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to clean up Docker resources
cleanup() {
    echo "Cleaning up Docker resources..."
    docker-compose down -v
}

# Function to build and start services
start_services() {
    echo "Building and starting services..."
    docker-compose up --build -d
}

# Function to show logs
show_logs() {
    docker-compose logs -f
}

# Main script
case "$1" in
    "start")
        check_docker
        start_services
        ;;
    "stop")
        cleanup
        ;;
    "logs")
        show_logs
        ;;
    "restart")
        cleanup
        start_services
        ;;
    *)
        echo "Usage: $0 {start|stop|logs|restart}"
        exit 1
        ;;
esac 