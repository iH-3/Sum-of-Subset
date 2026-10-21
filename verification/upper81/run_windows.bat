@echo off
setlocal
cd /d "%~dp0..\.."
where py >nul 2>nul
if errorlevel 1 (
  python -I -S -B verification\upper81\check.py --output results\local_upper81.json
) else (
  py -3 -I -S -B verification\upper81\check.py --output results\local_upper81.json
)
if errorlevel 1 (
  echo Verification failed. Review the error and detail logs.
  pause
  exit /b 1
)
echo Verification completed. See results\local_upper81.json.
pause
