@echo off
setlocal
cd /d "%~dp0"
python -I -S -B verification\upper82_work\check.py --output .work\upper82_c5t.json
if errorlevel 1 exit /b 1
python -I -S -B -O verification\upper82_work\check.py --output .work\upper82_c5t_O.json
if errorlevel 1 exit /b 1
fc /b .work\upper82_c5t.json .work\upper82_c5t_O.json
if errorlevel 1 exit /b 1
echo PASS_CONDITIONAL_C5T_SIZE83. Global upper bound remains 83.
