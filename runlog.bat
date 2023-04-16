@echo off
if not defined LANG set LANG=en
if not defined FORMAT set FORMAT=xlsx
if not defined ALLFORMAT set ALLFORMAT=false

:check_pip
pip install -r requirements.txt >nul
if %ERRORLEVEL% == 0 goto :start
echo "Checking pip error"
pause
exit

:start
if %ALLFORMAT% == "true" goto:start_all
python log.py -l %LANG% -f %FORMAT%
if %ERRORLEVEL% == 1 goto:error
goto:start

:start_all
python log.py -l %LANG% --all-formats
if %ERRORLEVEL% == 1 goto:start_all
goto:start

:error
echo "Error occurred"
pause
exit