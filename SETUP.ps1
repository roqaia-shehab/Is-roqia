# ============================================================================
#   AUTOMATED TIMETABLE GENERATION SYSTEM - QUICK SETUP
#   This script installs all dependencies and starts the server
# ============================================================================

Write-Host ""
Write-Host "========================================================================"
Write-Host "   AUTOMATED TIMETABLE GENERATION SYSTEM - QUICK SETUP"
Write-Host "========================================================================"
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] $pythonVersion" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.8+ from: https://www.python.org/downloads/"
    Write-Host "Make sure to check 'Add Python to PATH' during installation."
    Write-Host ""
    Pause
    exit 1
}

# Check if we're in the correct directory
if (-not (Test-Path "app.py")) {
    Write-Host "[ERROR] app.py not found!" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory."
    Write-Host ""
    Pause
    exit 1
}

Write-Host "[INFO] Installing dependencies..." -ForegroundColor Cyan
Write-Host ""

# Install Flask and Flask-CORS
try {
    python -m pip install --upgrade pip --quiet
    python -m pip install Flask==3.0.0 Flask-CORS==4.0.0
    
    if ($LASTEXITCODE -ne 0) {
        throw "pip install failed"
    }
    
    Write-Host ""
    Write-Host "========================================================================"
    Write-Host "   INSTALLATION COMPLETE!"
    Write-Host "========================================================================"
    Write-Host ""
    Write-Host "   Dependencies installed:" -ForegroundColor Green
    Write-Host "   - Flask 3.0.0"
    Write-Host "   - Flask-CORS 4.0.0"
    Write-Host ""
    Write-Host "   Starting server..."
    Write-Host ""
    Write-Host "========================================================================"
    Write-Host ""
    
    # Start the Flask server
    python app.py
    
} catch {
    Write-Host ""
    Write-Host "[ERROR] Failed to install dependencies!" -ForegroundColor Red
    Write-Host "Please check your internet connection and try again."
    Write-Host ""
    Write-Host "Error details: $_"
    Write-Host ""
    Pause
    exit 1
}

# If server exits with error
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Server failed to start!" -ForegroundColor Red
    Write-Host "Please check the error messages above."
    Write-Host ""
    Pause
    exit 1
}
