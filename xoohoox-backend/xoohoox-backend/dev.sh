#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Starting Xoohoox Backend Development Server...${NC}"

# Run the Python development script
python run_dev.py

# If the script exits with an error, show a message
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}The development server encountered an error.${NC}"
    echo -e "${YELLOW}Please check the logs for more information.${NC}"
    exit 1
fi 