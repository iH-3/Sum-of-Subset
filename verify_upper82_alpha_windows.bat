@echo off
setlocal
cd /d "%~dp0"
python -I -S -B verification\upper82_alpha\check.py --output .work\upper82_alpha.json
if errorlevel 1 exit /b 1
python -I -S -B -O verification\upper82_alpha\check.py --output .work\upper82_alpha_O.json
if errorlevel 1 exit /b 1
fc /b .work\upper82_alpha.json .work\upper82_alpha_O.json
if errorlevel 1 exit /b 1
echo PASS_CONDITIONAL_ALPHA_SIZE83. Global upper bound remains 83.
