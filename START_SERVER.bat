@echo off
REM ============================================================================
REM  Automated Timetable Generation System - Startup Script
REM ============================================================================

echo ================================================================================
echo  Automated Timetable Generation System
echo ================================================================================
echo.

cd /d "%~dp0"

echo Starting Flask server...
echo.
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
echo ================================================================================
echo.

REM Use the correct Python installation
"C:\Users\YAHOO COMPUTER\AppData\Local\Programs\Python\Python311\python.exe" app.py

pause
