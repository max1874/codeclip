#!/bin/bash

# Color definitions
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color
INFO="${BLUE}[INFO]${NC}"
SUCCESS="${GREEN}[SUCCESS]${NC}"
ERROR="${RED}[ERROR]${NC}"

echo -e "${INFO} Finding and terminating message.py process..."

# Find message.py process
PROCESS=$(pgrep -f "python.*message.py")

if [ -z "$PROCESS" ]; then
    echo -e "${INFO} No running message.py process found"
else
    echo -e "${INFO} Found process ID: $PROCESS"
    echo -e "${INFO} Terminating process..."
    kill $PROCESS
    
    # Check if the process was successfully terminated
    if ps -p $PROCESS > /dev/null; then
        echo -e "${ERROR} Cannot terminate process, trying force kill..."
        kill -9 $PROCESS
        
        if ps -p $PROCESS > /dev/null; then
            echo -e "${ERROR} Cannot force kill process, please terminate manually"
            exit 1
        else
            echo -e "${SUCCESS} Process force killed successfully"
        fi
    else
        echo -e "${SUCCESS} Process terminated successfully"
    fi
fi

echo -e "\n${SUCCESS} Operation completed! 👍" 