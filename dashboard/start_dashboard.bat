@echo off
echo Starting AI Traffic Management Dashboard...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Navigate to dashboard directory
cd /d "%~dp0"

REM Install dependencies if needed
if exist "requirements_dashboard.txt" (
    echo Installing dependencies...
    python -m pip install -r requirements_dashboard.txt --quiet
)

REM Create sample data if needed
python run_dashboard.py --setup-only

REM Launch dashboard
echo.
echo Opening dashboard in browser...
echo Dashboard will be available at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard
echo.

python run_dashboard.py --port 8501

pause
