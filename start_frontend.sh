#!/bin/bash
# Quick start script for frontend (Mac/Linux)

echo "Starting Git Commit Composer Frontend..."
echo ""

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    echo "This may take a few minutes..."
    echo ""
    npm install
fi

# Start the development server
echo ""
echo "Starting Vite development server on http://localhost:3000"
echo "Press Ctrl+C to stop"
echo ""
npm run dev
