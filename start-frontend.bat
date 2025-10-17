@echo off
echo 🚀 Starting Streetly Frontend...
echo.

REM Navigate to your frontend directory
cd /d "C:\Users\Maha\Downloads\stee\Streetly 4"

echo 📁 Serving from: %CD%
echo 🌐 Starting server on port 3001...
echo 🔗 Your frontend will be available at: http://localhost:3001
echo 🔗 Your backend should be running at: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo ----------------------------------------

REM Start the Python server
python serve.py
