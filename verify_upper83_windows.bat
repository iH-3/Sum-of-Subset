@echo off
cd /d "%~dp0"
py -3 -I -S -B verification\upper83_complete\check.py --output .work\upper83.json
if errorlevel 1 exit /b 1
pause
