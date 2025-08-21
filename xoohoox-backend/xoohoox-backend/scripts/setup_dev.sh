#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Setting up Xoohoox Backend Development Environment...${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Create necessary directories
echo -e "${YELLOW}Creating necessary directories...${NC}"
mkdir -p logs
mkdir -p app/tests
mkdir -p app/api/v1/endpoints

# Copy development environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.development .env
fi

# Run database migrations
echo -e "${YELLOW}Running database migrations...${NC}"
alembic upgrade head

# Create test user if it doesn't exist
echo -e "${YELLOW}Creating test user...${NC}"
python create_test_user.py

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
pytest

echo -e "${GREEN}Setup complete! You can now run the development server with:${NC}"
echo -e "${YELLOW}./dev.sh${NC}" 