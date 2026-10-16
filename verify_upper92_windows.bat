@echo off
cd /d "%~dp0"
py -3 -I -S -B verification\upper103.py --output .work\upper103.json
if errorlevel 1 goto failed
py -3 -I -S -B verification\upper100.py --output .work\upper100.json
if errorlevel 1 goto failed
py -3 -I -S -B verification\upper99.py --output .work\upper99.json
if errorlevel 1 goto failed
py -3 -I -S -B verification\upper98.py --output .work\upper98.json
if errorlevel 1 goto failed
py -3 -I -S -B verification\upper97_simplified.py --output .work\upper97_simplified.json
if errorlevel 1 goto failed
py -3 -I -S -B verification\upper96.py --output .work\upper96.json
if errorlevel 1 goto failed
py -3 -I -S -B verification\upper95.py --output .work\upper95.json
if errorlevel 1 goto failed
py -3 -I -S -B verification\upper94.py --output .work\upper94.json
if errorlevel 1 goto failed
py -3 -I -S -B verification\upper93.py --output .work\upper93.json
if errorlevel 1 goto failed
py -3 -I -S -B verification\upper92.py --output .work\upper92.json
if errorlevel 1 goto failed
echo All finite continuation checks passed. See the reports for the mathematical reductions.
pause
exit /b 0
:failed
echo Verification failed. This run does not establish the upper-bound certificate.
pause
exit /b 1
