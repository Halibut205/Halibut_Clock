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
echo "[INFO] Installing dependencies..."
pip3 install pygame

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install pygame"
    exit 1
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
echo "To run the app:"
echo "1. Run 'python3 main.py' from this directory"
echo "2. Or run './scripts/run.sh' (if executable)"
echo
read -p "Press Enter to continue..."
