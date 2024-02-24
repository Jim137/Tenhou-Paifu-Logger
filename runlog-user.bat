@echo off
rem.||(
Set skip_pip=true will skip check pip install

Set language after LANG=, default is English
English: en
Traditional Chinese: zh_tw
Simplified Chinese: zh
Japanese: ja

Set format after FORMAT=, default is csv
Excel: xlsx
html: html
csv: csv

Set ALLFORMAT=true to generate all formats

Set output directory after OUTPUT_DIR=, default is current directory

Set mjai=true to generate mjai format paifu
)

set skip_pip=

set LANG=
set FORMAT=
set ALLFORMAT=
set OUTPUT_DIR=
set mjai=

call runlog.bat
