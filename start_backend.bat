@echo off
REM Quick start script for backend (Windows)
echo Starting Git Commit Composer Backend...
echo.

cd backend

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if dependencies are installed
echo Checking dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your GEMINI_API_KEY
    echo.
    pause
    exit /b
)

REM Kill any process using port 8000
echo Checking if port 8000 is already in use...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Killing existing process on port 8000...
    taskkill /F /PID %%a 2>nul
)

REM Start the server
echo.
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop
echo.
python main.py

pause