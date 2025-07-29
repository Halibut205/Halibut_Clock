#!/bin/bash

echo "============================================"
echo "    Study Timer - Installation Script"
echo "============================================"
echo

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    *)          MACHINE="UNKNOWN:${OS}"
esac
echo "[INFO] Detected OS: ${MACHINE}"

# Check if Python is installed
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "[ERROR] Python is not installed"
        echo "3. pyenv: https://github.com/pyenv/pyenv"
    else
        echo "Please install Python 3.8+ from https://python.org"
    fi
    exit 1
fi

echo "[INFO] Python found"
$PYTHON_CMD --version

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "[INFO] Python version: $PYTHON_VERSION"

# Check pip
PIP_CMD=""
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "[WARNING] pip not found, trying to use python -m pip"
    PIP_CMD="$PYTHON_CMD -m pip"
fi

echo "[INFO] Using pip command: $PIP_CMD"

echo
echo "[INFO] Installing dependencies from requirements.txt..."

$PIP_CMD install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[WARNING] Failed to install dependencies from requirements.txt"
    echo "[INFO] Trying individual installations..."
    
    echo "[INFO] Installing pygame for audio..."
    $PIP_CMD install pygame
    if [ $? -ne 0 ]; then
        echo "[WARNING] Could not install pygame, app will use system beep"
    fi
    
    echo "[INFO] Installing matplotlib for charts..."
    $PIP_CMD install matplotlib
    if [ $? -ne 0 ]; then
        echo "[WARNING] Could not install matplotlib, charts will show placeholder"
    fi
else
    echo "[SUCCESS] All dependencies installed successfully!"
fi

echo
echo "[INFO] Creating data directory..."
mkdir -p data

echo
echo "[INFO] Checking sfx directory..."
mkdir -p sfx

if [ ! -f "sfx/button_1.mp3" ]; then
    echo "[WARNING] Sound file 'sfx/button_1.mp3' not found"
    echo "[INFO] App will run without sound effects"
    echo "[INFO] Add 'button_1.mp3' to 'sfx/' folder for sound"
fi

echo
echo "[SUCCESS] Setup completed!"
echo
echo "Features available:"
echo "- Timer with Pomodoro technique"
echo "- Daily statistics tracking"
echo "- Interactive charts and data visualization"
echo "- Sound effects (if pygame installed)"
echo "- Export functionality for data and charts"
echo
echo "To run the app:"
echo "1. Run '$PYTHON_CMD main.py' from this directory"
echo "2. Or run './run.sh' (make sure it's executable: chmod +x run.sh)"
echo
echo "To test charts functionality:"
echo "- Run '$PYTHON_CMD demos/demo_charts.py'"
echo
read -p "Press Enter to continue..."
