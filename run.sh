#!/bin/bash

echo "============================================"
echo "    Starting Fliqlo Timer..."
echo "============================================"

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Darwin*)    MACHINE=Mac;;
    *)          MACHINE="Other"
esac

# Find Python command
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "[ERROR] Python not found!"
    if [ "$MACHINE" = "Mac" ]; then
        echo "Try using: /usr/bin/python3 main.py"
    fi
    exit 1
fi

echo "[INFO] Using Python: $PYTHON_CMD"
echo "[INFO] Python version: $($PYTHON_CMD --version)"

# macOS specific setup
if [ "$MACHINE" = "Mac" ]; then
    echo "[INFO] Running on macOS"
    
    # Check tkinter
    $PYTHON_CMD -c "import tkinter" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "[WARNING] tkinter not available"
        echo "[INFO] Install with: brew install python-tk"
        echo "[INFO] Or use system Python: /usr/bin/python3 main.py"
    fi
    
    # Set display for better macOS compatibility
    export DISPLAY=:0
fi

# Change to script directory
cd "$(dirname "$0")"

echo "[INFO] Starting application..."
echo

$PYTHON_CMD main.py

echo
echo "[INFO] Application closed."
