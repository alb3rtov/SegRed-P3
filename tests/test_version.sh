#!/bin/bash

curl -s http://127.0.0.1:5000/ &> /dev/null

if [ $? -ne 0 ]; then
    echo "Server is not active"
    exit 1
fi

output=$(curl -s http://127.0.0.1:5000/version | jq .version 2> /dev/null)

if [ $? -ne 0 ]; then
    echo "Bad request :("
    exit 1
fi 

if [[ $output != "null" ]]; then
    echo "Version: $(echo $output | tr -d '"')"
    exit 0
else
    echo "Bad request :("
    exit 1
fi