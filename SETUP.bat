@echo off
REM ============================================================================
REM   AUTOMATED TIMETABLE GENERATION SYSTEM - QUICK SETUP
REM   This script installs all dependencies and starts the server
REM ============================================================================

echo.
echo ========================================================================
echo    AUTOMATED TIMETABLE GENERATION SYSTEM - QUICK SETUP
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check if we're in the correct directory
if not exist "app.py" (
    echo [ERROR] app.py not found!
    echo Please run this script from the project root directory.
    echo.
    pause
    exit /b 1
)

echo [INFO] Installing dependencies...
echo.

REM Install Flask and Flask-CORS
python -m pip install --upgrade pip >nul 2>&1
python -m pip install Flask==3.0.0 Flask-CORS==4.0.0

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies!
    echo Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo   INSTALLATION COMPLETE!
echo ========================================================================
echo.
echo   Dependencies installed:
echo   - Flask 3.0.0
echo   - Flask-CORS 4.0.0
echo.
echo   Starting server...
echo.
echo ========================================================================
echo.

REM Start the Flask server
python app.py

REM If server exits with error
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Server failed to start!
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)
