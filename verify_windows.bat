@echo off
cd /d "%~dp0"
py -3 verification\verify.py --output .work\independent.json
set "verify_status=%errorlevel%"
pause
exit /b %verify_status%
