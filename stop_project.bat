@echo off
setlocal
title Legal Education AI Platform - Shutdown

echo ===========================================
echo Stopping Legal Education AI Platform...
echo ===========================================

echo Stopping backend on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a > nul 2>&1

echo Stopping frontend on port 8501...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501 ^| findstr LISTENING') do taskkill /F /PID %%a > nul 2>&1

echo Done! All related processes have been stopped.
echo ===========================================
pause
