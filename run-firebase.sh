#!/bin/bash

# Script to run Firebase Hosting for Streetly Frontend
echo "🚀 Starting Firebase Hosting for Streetly Frontend..."

# Navigate to the firebase directory
cd "/Users/Maha/Downloads/stee/firebase"

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

# Start Firebase hosting
echo "🌐 Starting Firebase Hosting on port 5000..."
echo "📁 Serving files from: /Users/Maha/Downloads/stee/Streetly 4/"
echo "🔗 Access your frontend at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"

firebase serve --only hosting
