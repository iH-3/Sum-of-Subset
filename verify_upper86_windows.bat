@echo off
setlocal
cd /d "%~dp0"
py -3 -I -S -B verification\upper86.py --jobs 4 --output results\local-upper86.json
if errorlevel 1 exit /b 1
echo Complete finite endpoint verification passed. See the report for the mathematical reductions.
