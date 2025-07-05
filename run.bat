@echo off
echo Starting Fliqlo Timer...

REM Try virtual environment first, then fallback to system Python
if exist ".venv\Scripts\python.exe" (
    echo Using virtual environment...
    ".venv\Scripts\python.exe" main.py
) else (
    echo Using system Python...
    python main.py
)

pause
