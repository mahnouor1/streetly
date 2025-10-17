#!/bin/bash

# Streetly Travel Assistant - Firebase Deployment Script
# This script automates the deployment process to Firebase Hosting

echo "🚀 Streetly Travel Assistant - Firebase Deployment"
echo "=================================================="

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Installing..."
    npm install -g firebase-tools
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Firebase CLI. Please install manually:"
        echo "   npm install -g firebase-tools"
        exit 1
    fi
    echo "✅ Firebase CLI installed successfully"
else
    echo "✅ Firebase CLI found"
fi

# Check if user is logged in
if ! firebase projects:list &> /dev/null; then
    echo "🔐 Please login to Firebase..."
    firebase login
    if [ $? -ne 0 ]; then
        echo "❌ Firebase login failed"
        exit 1
    fi
else
    echo "✅ Firebase authentication verified"
fi

# Check if firebase.json exists
if [ ! -f "firebase.json" ]; then
    echo "❌ firebase.json not found. Please run this script from the project root."
    exit 1
fi

# Check if .firebaserc exists
if [ ! -f ".firebaserc" ]; then
    echo "❌ .firebaserc not found. Please configure your Firebase project:"
    echo "   firebase use --add"
    exit 1
fi

# Check if Streetly 4 directory exists
if [ ! -d "Streetly 4" ]; then
    echo "❌ 'Streetly 4' directory not found. Please ensure frontend files are present."
    exit 1
fi

echo "📁 Project structure verified"

# Deploy to Firebase
echo "🚀 Deploying to Firebase Hosting..."
firebase deploy --only hosting

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deployment successful!"
    echo "🌐 Your Streetly Travel Assistant is now live!"
    echo ""
    echo "📋 Next steps:"
    echo "   - Check your Firebase Console for the live URL"
    echo "   - Test all features on the live site"
    echo "   - Set up custom domain if needed"
    echo "   - Configure analytics and monitoring"
    echo ""
    echo "🔗 Firebase Console: https://console.firebase.google.com/"
else
    echo "❌ Deployment failed. Please check the error messages above."
    exit 1
fi
