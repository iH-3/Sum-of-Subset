@echo off
setlocal
cd /d "%~dp0\..\.."
py -3 -I -S -B verification\upper82_global\check.py --output results\local_upper82.json
if errorlevel 1 goto failed
echo Complete finite replay passed. Read the companion report for the mathematical proof.
pause
exit /b 0
:failed
echo Verification failed. Please read the error above.
pause
exit /b 1
