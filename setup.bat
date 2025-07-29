@echo off
echo ============================================
echo    Study Timer - Installation Script
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [INFO] Python found
python --version

echo.
echo [INFO] Installing dependencies from requirements.txt...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [WARNING] Could not install all dependencies from requirements.txt
    echo [INFO] Trying individual installations...
    
    echo [INFO] Installing pygame for button sounds...
    pip install pygame
    
    if %errorlevel% neq 0 (
        echo [WARNING] Could not install pygame
        echo [INFO] Buttons will work without sound
    )
    
    echo [INFO] Installing matplotlib for charts...
    pip install matplotlib
    
    if %errorlevel% neq 0 (
        echo [WARNING] Could not install matplotlib
        echo [INFO] Charts will show placeholder text
    )
) else (
    echo [SUCCESS] All dependencies installed successfully!
)

echo.
echo [INFO] Creating data directory...
if not exist "data" mkdir data

echo.
echo [INFO] Checking sfx directory...
if not exist "sfx" mkdir sfx

if not exist "sfx\button_1.mp3" (
    echo [WARNING] Sound file 'sfx\button_1.mp3' not found
    echo [INFO] Add 'button_1.mp3' to 'sfx\' folder for button sounds
)

if not exist "sfx\whitenoise_1.mp3" (
    echo [WARNING] Background music 'sfx\whitenoise_1.mp3' not found
    echo [INFO] Add 'whitenoise_1.mp3' to 'sfx\' folder for background music
    echo [INFO] App will work without background music
)

echo.
echo [SUCCESS] Setup completed!
echo.
echo Features available:
echo - Timer with Pomodoro technique
echo - Daily statistics tracking
echo - Interactive charts and data visualization
echo - Sound effects (if pygame installed)
echo - Export functionality for data and charts
echo.
echo To run the app:
echo 1. Double-click 'run.bat'
echo 2. Or run 'python main.py' from this directory
echo.
echo To test charts functionality:
echo - Run 'python quick_test_matplotlib.py'
echo - Or run 'python demo_charts.py'
echo.
pause
