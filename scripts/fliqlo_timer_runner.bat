@echo off
cd /d "%~dp0\.."
echo Starting Fliqlo Timer...
python main.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to run the application
    echo Make sure Python is installed and pygame is available
    echo Run 'setup.bat' first if this is your first time
)
pause
