# !/bin/bash
###########################################
# If error "command not found" occurs on wsl,
# please uncomment the followings.

# dos2unix runlog-user.sh
# dos2unix runlog.sh

###########################################

#########################################################
# Uncomment and change the variables below to your need:#
#########################################################

# python3 executable
#python_cmd="python3"

# Set skip_pip=true will skip check pip install
# export skip_pip=

# Set language after LANG=, default is English
# English: en
# Traditional Chinese: zh_tw
# Simplified Chinese: zh
# Japanese: ja
# export LANG=

# Set format after FORMAT=, default is csv
# Excel: xlsx
# html: html
# csv: csv
# export FORMAT=

# Set ALLFORMAT=true to generate all formats
# export ALLFORMAT=

# Set output directory after OUTPUT_DIR=, default is current directory
# export OUTPUT_DIR=

# Set mjai=true to generate mjai format paifu
# export mjai=
###########################################

. runlog.sh
