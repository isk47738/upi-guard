@echo off
title UPI Guard - Real vs Fake Payment Scanner
cd /d "%~dp0"
start "UPI Guard Server" cmd /k "python server.py"
timeout /t 2 >nul
start msedge --app="http://localhost:8000/fast_scanner.html" --window-size=450,850 2>nul || start chrome --app="http://localhost:8000/fast_scanner.html" --window-size=450,850 2>nul || start http://localhost:8000/fast_scanner.html
