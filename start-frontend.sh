#!/bin/bash

echo "🚀 Starting Streetly Frontend..."
echo ""

# Kill any existing servers on port 3001
echo "🔄 Checking for existing servers..."
lsof -ti:3001 | xargs kill -9 2>/dev/null || true

# Navigate to your frontend directory
cd "/Users/Maha/Downloads/stee/Streetly 4"

echo "📁 Serving from: $(pwd)"
echo "🌐 Starting server on port 3001..."
echo "🔗 Your frontend will be available at: http://localhost:3001"
echo "🔗 Your backend should be running at: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo "----------------------------------------"

# Start the Python server
python3 serve.py
