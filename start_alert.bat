@echo off
echo ============================================
echo Simple Alert System - One Command Launcher
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Starting Simple Alert System...
echo.

REM Run the Python launcher
python start_alert_system.py

echo.
echo System stopped. Press any key to exit...
pause >nul
