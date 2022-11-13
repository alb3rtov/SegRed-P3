#!/bin/bash

if [ ! -d ".env" ]; then
  $(which python3) -m venv .venv
fi

source .venv/bin/activate

pip list | grep Flask-RESTful &> /dev/null
status_code=$?

if [ $status_code -ne 0 ]; then
  pip install -r requirements.txt
fi
