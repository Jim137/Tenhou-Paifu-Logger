@echo off
rem.||(
Set skip_pip=true will skip check pip install

Set language after LANG=, default is English
Traditional Chinese: zh_tw

Set format after FORMAT=, default is Excel
Excel: xlsx
html: html

Set ALLFORMAT=true to generate all formats
)

set skip_pip=

set LANG=
set FORMAT=
set ALLFORMAT=

call runlog.bat
