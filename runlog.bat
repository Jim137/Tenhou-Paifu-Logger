@echo off
if not defined skip_pip set skip_pip=false
if not defined LANG set LANG=en
if not defined FORMAT set FORMAT=csv
if not defined ALLFORMAT set ALLFORMAT=false
if not defined OUTPUT_DIR set OUTPUT_DIR=./
if not defined mjai set mjai=false

if %ALLFORMAT% == true (
set args=-l %LANG% --all-formats -o %OUTPUT_DIR%
) else (
    set args=-l %LANG% -f %FORMAT% -o %OUTPUT_DIR%
)
if %mjai% == true set args=%args% --mjai

if %skip_pip% == true goto :start

:check_pip
pip install -r requirements.txt >nul
if %ERRORLEVEL% == 0 goto :start
echo "Checking pip error"
pause
exit

:start
python launch.py %args%
if %ERRORLEVEL% == 1 goto:error
goto:start

:error
echo "Error occurred"
pause
exit
