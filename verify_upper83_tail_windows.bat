@echo off
setlocal
cd /d "%~dp0"
python -I -S -B verification\upper83_tail.py --output .work\upper83_tail.json
if errorlevel 1 exit /b 1
python -I -S -B -O verification\upper83_tail.py --output .work\upper83_tail_O.json
if errorlevel 1 exit /b 1
fc /b .work\upper83_tail.json .work\upper83_tail_O.json
if errorlevel 1 exit /b 1
echo PASS_CONDITIONAL_GEOMETRIC_FAMILY. Global upper bound remains 84.
