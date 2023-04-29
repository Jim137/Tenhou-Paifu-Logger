@echo off
if not defined skip_pip set set skip_pip=false
if not defined LANG set LANG=en
if not defined FORMAT set FORMAT=xlsx
if not defined ALLFORMAT set ALLFORMAT=false

if %skip_pip% == true goto :start

:check_pip
pip install -r requirements.txt >nul
if %ERRORLEVEL% == 0 goto :start
echo "Checking pip error"
pause
exit

:start
if %ALLFORMAT% == true goto:start_all
python log.py -l %LANG% -f %FORMAT%
if %ERRORLEVEL% == 1 goto:error
goto:start

:start_all
python log.py -l %LANG% --all-formats
if %ERRORLEVEL% == 1 goto:error
goto:start_all

:error
echo "Error occurred"
pause
exit