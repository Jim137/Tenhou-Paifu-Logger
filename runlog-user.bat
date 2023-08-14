@echo off
rem.||(
Set skip_pip=true will skip check pip install

Set language after LANG=, default is English
Traditional Chinese: zh_tw

Set format after FORMAT=, default is Excel
Excel: xlsx
html: html

Set ALLFORMAT=true to generate all formats

Set output directory after OUTPUT_DIR=, default is current directory
)

set skip_pip=

set LANG=
set FORMAT=
set ALLFORMAT=
set OUTPUT_DIR=

call runlog.bat
