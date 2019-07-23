#!/usr/bin/env bash

if command -v python3 &>/dev/null; then
    pip3 install -r requirements.txt
    cd Interface
    flask run
else
    echo Python 3 is not installed
fi
