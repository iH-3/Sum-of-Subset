@echo off
setlocal
cd /d "%~dp0"
py -3 -I -S -B verification\upper87_geometry.py --output results\local_upper87_geometry.json
if errorlevel 1 exit /b 1
py -3 -I -S -B verification\upper87.py --jobs 4 --output results\local_upper87.json
if errorlevel 1 exit /b 1
echo Complete size-88 finite replay passed. See the report for the mathematical reduction.
endlocal
