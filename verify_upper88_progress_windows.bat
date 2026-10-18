@echo off
setlocal
cd /d "%~dp0"
py -3 -I -S -B verification/upper88_progress.py --output .work/upper88-progress.json
if errorlevel 1 goto fail
py -3 -I -S -B experiments/verify_upper88_geometric_rows.py --output .work/upper88-geometric-rows.json
if errorlevel 1 goto fail
echo Progress verified. The audited global upper bound remains 89; 88 is NOT proved.
pause
exit /b 0
:fail
echo Verification failed.
pause
exit /b 1
