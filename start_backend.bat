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

REM Start the server
echo.
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop
echo.
python main.py

pause