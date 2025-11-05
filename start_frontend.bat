@echo off
REM Quick start script for frontend (Windows)
echo Starting Git Commit Composer Frontend...
echo.

cd frontend

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Installing dependencies...
    echo This may take a few minutes...
    echo.
    npm install
)

REM Start the development server
echo.
echo Starting Vite development server on http://localhost:3000
echo Press Ctrl+C to stop
echo.
npm run dev
