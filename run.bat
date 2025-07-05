@echo off

REM Run with hidden console window
REM Try virtual environment first, then fallback to system Python
if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" main.py
) else if exist ".venv\Scripts\python.exe" (
    start "" /min ".venv\Scripts\python.exe" main.py
) else (
    start "" /min python main.py
)
