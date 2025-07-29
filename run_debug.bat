@echo off
echo ============================================
echo    Study Timer - Debug Mode
echo ============================================
echo.

REM Debug mode with visible console
REM Try virtual environment first, then fallback to system Python
if exist ".venv\Scripts\python.exe" (
    echo [DEBUG] Using virtual environment...
    ".venv\Scripts\python.exe" main.py
) else (
    echo [DEBUG] Using system Python...
    python main.py
)

echo.
echo [DEBUG] Application closed.
pause
