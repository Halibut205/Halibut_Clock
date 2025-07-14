#!/bin/bash

echo "============================================"
echo "    Fliqlo Timer - Installation Script"
echo "============================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

echo "[INFO] Python found"
python3 --version

echo
echo "[INFO] Installing dependencies from requirements.txt..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[WARNING] Failed to install dependencies from requirements.txt"
    echo "[INFO] Trying individual installations..."
    
    echo "[INFO] Installing pygame for audio..."
    pip3 install pygame
    if [ $? -ne 0 ]; then
        echo "[WARNING] Could not install pygame, app will use system beep"
    fi
    
    echo "[INFO] Installing matplotlib for charts..."
    pip3 install matplotlib
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
echo "1. Run 'python3 main.py' from this directory"
echo "2. Or run './run.sh' (if available)"
echo
echo "To test charts functionality:"
echo "- Run 'python3 quick_test_matplotlib.py'"
echo "- Or run 'python3 demo_charts.py'"
echo
read -p "Press Enter to continue..."
