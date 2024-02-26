#!/bin/bash

check_pip() {
    pip install -r requirements.txt > /dev/null
    if [ $? = 0 ]; then
            start
    fi
    printf "Checking pip error"
    exit 1
}

start() {
    "${python_cmd}" launch.py $args
    if [ $? != 0 ]
    then
        printf "Error occurred"
        exit 1
    fi
    start
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
    FORMAT=csv
fi
if [ -z $ALLFORMAT ]
then
    ALLFORMAT=false
fi
if [ -z $OUTPUT_DIR ]
then
    OUTPUT_DIR=./
fi
if [ -z $mjai ]
then
    mjai=false
fi

if [ $ALLFORMAT = true ]
    then args="-l $LANG --all-formats -o $OUTPUT_DIR"
    else args="-l $LANG -f $FORMAT -o $OUTPUT_DIR"
fi
if [ $mjai = true ]
    then args="$args --mjai"
fi

if [ $skip_pip = true ]
then
    start
else
    check_pip
fi
