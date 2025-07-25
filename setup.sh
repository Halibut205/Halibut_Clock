#!/bin/bash

echo "============================================"
echo "    Fliqlo Timer - Installation Script"
echo "============================================"
echo

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
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
    if [ "$MACHINE" = "Mac" ]; then
        echo "Please install Python 3.8+ using one of these methods:"
        echo "1. Homebrew: brew install python"
        echo "2. Official installer: https://python.org"
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

# macOS specific fixes
if [ "$MACHINE" = "Mac" ]; then
    echo "[INFO] Applying macOS-specific configurations..."
    
    # Check if Xcode command line tools are installed (needed for some packages)
    if ! xcode-select -p &> /dev/null; then
        echo "[WARNING] Xcode command line tools not found"
        echo "[INFO] Installing Xcode command line tools..."
        xcode-select --install
        echo "[INFO] Please wait for installation to complete and run this script again"
        exit 1
    fi
    
    # For macOS, ensure we have tkinter
    $PYTHON_CMD -c "import tkinter" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "[WARNING] tkinter not found"
        echo "[INFO] If using Homebrew Python, install with: brew install python-tk"
        echo "[INFO] If using pyenv, reinstall Python with: env PYTHON_CONFIGURE_OPTS='--with-tcltk-includes=-I$(brew --prefix tcl-tk)/include' pyenv install 3.x.x"
    fi
fi

$PIP_CMD install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[WARNING] Failed to install dependencies from requirements.txt"
    echo "[INFO] Trying individual installations..."
    
    echo "[INFO] Installing pygame for audio..."
    $PIP_CMD install pygame
    if [ $? -ne 0 ]; then
        echo "[WARNING] Could not install pygame, app will use system beep"
        if [ "$MACHINE" = "Mac" ]; then
            echo "[INFO] On macOS, you might need to install SDL2 first:"
            echo "       brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf"
        fi
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
if [ "$MACHINE" = "Mac" ]; then
    echo "1. Run '$PYTHON_CMD main.py' from this directory"
    echo "2. Or run './run.sh' (make sure it's executable: chmod +x run.sh)"
    echo "3. On macOS, the app window might appear behind other windows"
else
    echo "1. Run '$PYTHON_CMD main.py' from this directory"
    echo "2. Or run './run.sh' (make sure it's executable: chmod +x run.sh)"
fi
echo
echo "To test charts functionality:"
echo "- Run '$PYTHON_CMD demos/demo_charts.py'"
echo
if [ "$MACHINE" = "Mac" ]; then
    echo "macOS Notes:"
    echo "- If you get 'command not found' errors, try: /usr/bin/python3 main.py"
    echo "- If tkinter issues occur, install python-tk: brew install python-tk"
    echo "- For sound issues, install SDL2: brew install sdl2 sdl2_mixer"
    echo
fi
read -p "Press Enter to continue..."
