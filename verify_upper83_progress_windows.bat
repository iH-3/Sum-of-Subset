@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 goto use_python
py -3 -I -S -B verification\upper83_progress.py --output .work\upper83_progress.json
exit /b %errorlevel%
:use_python
python -I -S -B verification\upper83_progress.py --output .work\upper83_progress.json
exit /b %errorlevel%
