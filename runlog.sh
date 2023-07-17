#!/bin/bash

# python3 executable
if [[ -z "${python_cmd}" ]]; then
    python_cmd="python3"
fi
if [ -z "$skip_pip" ]; then
    skip_pip=false
fi
if [ -z "$LANG" ]; then
    LANG=en
fi
if [ -z "$FORMAT" ]; then
    FORMAT=html
fi
if [ -z "$ALLFORMAT" ]; then
    ALLFORMAT=false
fi

if [ "$skip_pip" = true ]; then
    start
else
    check_pip
fi

check_pip() {
    pip install -r requirements.txt > /dev/null
    if [ $? -eq 0 ]; then
        start
    fi
    printf "Checking pip error"
    exit 1
}

start() {
    if [ "$ALLFORMAT" = true ]; then
        start_all
    fi
    "${python_cmd}" log.py -l "$LANG" -f "$FORMAT"
    if [ $? -eq 1 ]; then
        printf "Error occurred"
        exit 1
    fi
    start
}

start_all() {
    "${python_cmd}" log.py -l "$LANG" --all-formats
    if [ $? -eq 1 ]; then
        error
    fi
    start_all
}