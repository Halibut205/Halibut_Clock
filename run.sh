#!/bin/bash

echo "============================================"
echo "    Starting Study Timer..."
echo "============================================"

# Find Python command
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "[ERROR] Python not found!"
    exit 1
fi

echo "[INFO] Using Python: $PYTHON_CMD"
echo "[INFO] Python version: $($PYTHON_CMD --version)"

# Change to script directory
cd "$(dirname "$0")"

echo "[INFO] Starting application..."
echo

$PYTHON_CMD main.py

echo
echo "[INFO] Application closed."
