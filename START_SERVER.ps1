# ============================================================================
# Automated Timetable Generation System - PowerShell Startup Script
# ============================================================================

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host " Automated Timetable Generation System" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

Write-Host "✓ Starting Flask server..." -ForegroundColor Green
Write-Host ""
Write-Host "📍 Server will be available at: http://localhost:5000" -ForegroundColor Yellow
Write-Host "🌐 Open this URL in your browser to use the application" -ForegroundColor Yellow
Write-Host "⏹️  Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Use the correct Python installation (adjust path if needed)
$pythonPath = "C:\Users\YAHOO COMPUTER\AppData\Local\Programs\Python\Python311\python.exe"

if (Test-Path $pythonPath) {
    & $pythonPath app.py
} else {
    Write-Host "❌ Error: Python not found at: $pythonPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Trying alternative methods..." -ForegroundColor Yellow
    
    # Try to find Python automatically
    $foundPython = (Get-Command python -ErrorAction SilentlyContinue).Source
    if ($foundPython) {
        Write-Host "✓ Found Python at: $foundPython" -ForegroundColor Green
        & python app.py
    } else {
        Write-Host "❌ Could not find Python installation" -ForegroundColor Red
        Write-Host "Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
