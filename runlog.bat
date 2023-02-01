@echo off
if not defined LANG set LANG=en

:check_pip
pip install -r requirements.txt >nul
if %ERRORLEVEL% == 0 goto :start
echo "checking pip error"
pause
exit

:start
python log.py %LANG%
goto:start