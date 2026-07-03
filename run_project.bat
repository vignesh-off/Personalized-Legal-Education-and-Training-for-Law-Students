@echo off
setlocal
title Legal Education AI Platform Launcher

echo ===========================================
echo Starting Legal Education AI Platform
echo ===========================================

:: Change directory to the location of this batch file
cd /d "%~dp0"

if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found.
    echo Please run this file from the project folder.
    pause
    exit /b 1
)

echo [1/5] Checking Python...
where python > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not added to PATH.
    echo Install Python 3.10 or newer, then run this file again.
    pause
    exit /b 1
)

echo [2/5] Preparing virtual environment...
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
)

echo [3/5] Installing project dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

echo [4/5] Starting FastAPI Backend on Port 8000...
start "FastAPI Backend" /D "%~dp0" cmd /k ".venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

:: Wait 8 seconds to let backend fully initialize
timeout /t 8 /nobreak > nul

echo [5/5] Starting Streamlit Frontend...
start "Streamlit Frontend" /D "%~dp0" cmd /k ".venv\Scripts\python.exe -m streamlit run frontend.py"

echo Setup complete! Keep the terminal windows open while presenting.
pause
exit
