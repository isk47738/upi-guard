@echo off
title UPI Guard - Live Server & App Launcher
cd /d "%~dp0"
cls
echo =================================================================
echo   🛡️  UPI GUARD - FAKE UPI PAYMENT DETECTOR
echo =================================================================
echo.
echo [1/2] Python Server shuru ho raha hai...
start "UPI Guard Server" cmd /k "python server.py"

timeout /t 2 >nul

echo [2/2] Dedicated Mobile-view App khul rahi hai...
start msedge --app="http://localhost:8000/fast_scanner.html" --window-size=440,860 2>nul || start chrome --app="http://localhost:8000/fast_scanner.html" --window-size=440,860 2>nul || start http://localhost:8000/fast_scanner.html

echo.
echo =================================================================
echo   ✅ AAPKA APP LAPTOP PE KHUL GAYA HAI!
echo.
echo   📱 PHONE PE CHALANE KE LIYE (Mobile Tethering):
echo   👉 Phone ke Chrome browser me ye link daalo:
echo      Server window me dikhne wala Phone / Wi-Fi link use karein.
echo =================================================================
echo.
pause
