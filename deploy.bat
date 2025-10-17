@echo off
REM Streetly Travel Assistant - Firebase Deployment Script (Windows)
REM This script automates the deployment process to Firebase Hosting

echo 🚀 Streetly Travel Assistant - Firebase Deployment
echo ==================================================

REM Check if Firebase CLI is installed
firebase --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Firebase CLI not found. Installing...
    npm install -g firebase-tools
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Firebase CLI. Please install manually:
        echo    npm install -g firebase-tools
        pause
        exit /b 1
    )
    echo ✅ Firebase CLI installed successfully
) else (
    echo ✅ Firebase CLI found
)

REM Check if user is logged in
firebase projects:list >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔐 Please login to Firebase...
    firebase login
    if %errorlevel% neq 0 (
        echo ❌ Firebase login failed
        pause
        exit /b 1
    )
) else (
    echo ✅ Firebase authentication verified
)

REM Check if firebase.json exists
if not exist "firebase.json" (
    echo ❌ firebase.json not found. Please run this script from the project root.
    pause
    exit /b 1
)

REM Check if .firebaserc exists
if not exist ".firebaserc" (
    echo ❌ .firebaserc not found. Please configure your Firebase project:
    echo    firebase use --add
    pause
    exit /b 1
)

REM Check if Streetly 4 directory exists
if not exist "Streetly 4" (
    echo ❌ 'Streetly 4' directory not found. Please ensure frontend files are present.
    pause
    exit /b 1
)

echo 📁 Project structure verified

REM Deploy to Firebase
echo 🚀 Deploying to Firebase Hosting...
firebase deploy --only hosting

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Deployment successful!
    echo 🌐 Your Streetly Travel Assistant is now live!
    echo.
    echo 📋 Next steps:
    echo    - Check your Firebase Console for the live URL
    echo    - Test all features on the live site
    echo    - Set up custom domain if needed
    echo    - Configure analytics and monitoring
    echo.
    echo 🔗 Firebase Console: https://console.firebase.google.com/
) else (
    echo ❌ Deployment failed. Please check the error messages above.
    pause
    exit /b 1
)

pause
