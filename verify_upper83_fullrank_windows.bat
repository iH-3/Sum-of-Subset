@echo off
setlocal
cd /d "%~dp0"
python -I -S -B verification\upper83_fullrank\check.py --output .work\upper83_fullrank.json
if errorlevel 1 exit /b 1
python -I -S -B -O verification\upper83_fullrank\check.py --output .work\upper83_fullrank_O.json
if errorlevel 1 exit /b 1
fc /b .work\upper83_fullrank.json .work\upper83_fullrank_O.json
if errorlevel 1 exit /b 1
echo PASS_CONDITIONAL_PROGRESS_ONLY. Global upper bound remains 84.
