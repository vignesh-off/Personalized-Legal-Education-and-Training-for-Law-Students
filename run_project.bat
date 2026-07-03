@echo off
setlocal
title Legal Education AI Platform Launcher

echo ===========================================
echo Starting Legal Education AI Platform
echo ===========================================

:: Start from the project root directory
cd /d "%~dp0"

echo [1/8] Checking for Python 3.11...
py -3.11 --version > nul 2>&1
if errorlevel 1 (
    echo Python 3.11 is required. Please install Python 3.11 and enable Add to PATH.
    pause
    exit /b 1
)
echo Python 3.11 found.

echo [2/8] Setting up local virtual environment (.venv)...
if not exist ".venv" (
    echo Creating new virtual environment using Python 3.11...
    py -3.11 -m venv .venv
) else (
    echo Virtual environment already exists.
)

echo [3/8] Activating .venv...
call .venv\Scripts\activate
set PYTHONNOUSERSITE=1

echo [4/8] Upgrading pip, setuptools, wheel...
.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel > nul

echo [5/8] Installing critical binary wheels first...
.venv\Scripts\python.exe -m pip install --only-binary=:all: --no-cache-dir numpy==1.26.4 pandas==2.2.2 pydantic==2.8.2 pydantic-core==2.20.1
if errorlevel 1 (
    echo Wrong Python version or architecture. Use 64-bit Python 3.11.
    pause
    exit /b 1
)

echo [6/8] Installing requirements...
.venv\Scripts\python.exe -m pip install --only-binary=:all: --no-cache-dir -r requirements.txt
if errorlevel 1 (
    echo Wrong Python version or architecture. Use 64-bit Python 3.11.
    pause
    exit /b 1
)

echo [7/8] Verifying imports...
.venv\Scripts\python.exe -c "import numpy, pandas, pydantic, fastapi, streamlit; print('Dependencies OK')"
if errorlevel 1 (
    echo ERROR: Dependency verification failed.
    pause
    exit /b 1
)

echo [8/8] Starting Application...
echo Stopping any existing processes on ports 8000 and 8501...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a > nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501 ^| findstr LISTENING') do taskkill /F /PID %%a > nul 2>&1
echo Starting backend on port 8000...
start "Legal Backend" cmd /c "call .venv\Scripts\activate && .venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

echo Waiting 5 seconds for backend to initialize...
timeout /t 5 /nobreak > nul

echo Starting frontend on port 8501...
start "Legal Frontend" cmd /c "call .venv\Scripts\activate && .venv\Scripts\python.exe -m streamlit run frontend.py --server.port 8501"

echo Waiting 5 seconds for frontend to initialize...
timeout /t 5 /nobreak > nul

echo Open the app manually at: http://localhost:8501

echo ===========================================
echo Platform is now running!
echo Backend is running in the "Legal Backend" window.
echo Frontend is running in the "Legal Frontend" window.
echo Close those windows or use stop_project.bat to stop the platform.
echo ===========================================
pause
