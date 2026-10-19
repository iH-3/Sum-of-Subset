@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
  py -3 -I -S -B verification\upper84_adoption.py --output .work\upper84_replay.json
) else (
  python -I -S -B verification\upper84_adoption.py --output .work\upper84_replay.json
)
set "verify_result=%errorlevel%"
echo Exit code: %verify_result%
pause
exit /b %verify_result%
