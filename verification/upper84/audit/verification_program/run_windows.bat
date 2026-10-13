@echo off
setlocal
cd /d "%~dp0"
py -3 --version >nul 2>&1
if not errorlevel 1 (
  py -3 verify.py --full %*
  goto finish
)
python --version >nul 2>&1
if not errorlevel 1 (
  python verify.py --full %*
  goto finish
)
echo Python 3.10 or later is required. Install Python and then run this file again.
set "RC=1"
goto end
:finish
set "RC=%ERRORLEVEL%"
:end
echo.
if not "%RC%"=="0" echo Verification did not complete successfully. Read the messages above.
pause
exit /b %RC%
