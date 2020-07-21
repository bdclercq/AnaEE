#!/usr/bin/env bash

if command -v flask &>/dev/null; then
  echo Flask found
else
  sudo apt install python3-flask
fi

if command -v python3 &>/dev/null; then
    pip3 install -r requirements.txt
    cd Interface
    flask run
else
    echo Python 3 is not installed
fi
