#!/bin/bash

check_pip() {
    pip install -r requirements.txt > /dev/null
    if [ $? = 0 ]; then
        if [ $ALLFORMAT = true ]
        then
            start_all
        else
            start
        fi
    fi
    printf "Checking pip error"
    exit 1
}

start() {
    "${python_cmd}" log.py -l "$LANG" -f "$FORMAT"
    if [ $? != 0 ]
    then
        printf "Error occurred"
        exit 1
    fi
    start
}

start_all() {
    "${python_cmd}" log.py -l "$LANG" --all-formats
    if [ $? != 0 ]
    then
        printf "Error occurred"
        exit 1
    fi
    start_all
}

# python3 executable
if [[ -z $python_cmd ]]
then
    python_cmd="python3"
fi
if [ -z $skip_pip ]
then
    skip_pip=false
fi
if [ -z $LANG ]
then
    LANG=en
fi
if [ -z $FORMAT ]
then
    FORMAT=html
fi
if [ -z $ALLFORMAT ]
then
    ALLFORMAT=false
fi

if [ $skip_pip = true ]
then
    start
else
    check_pip
fi
