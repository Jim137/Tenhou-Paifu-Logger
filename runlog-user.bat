@echo off
rem.||(
Set language after LANG=, default is English
Traditional Chinese: zh_tw

Set format after FORMAT=, default is Excel
Excel: xlsx
html: html

Set ALLFORMAT=true to generate all formats
)

set LANG=
set FORMAT=
set ALLFORMAT=

call runlog.bat
