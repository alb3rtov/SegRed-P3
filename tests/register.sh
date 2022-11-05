#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
    echo -ne "Usage: ./test_register_login.sh <user> <password>\n"
    exit 1
fi

curl -s http://127.0.0.1:5000/ &> /dev/null

if [ $? -ne 0 ]; then
    echo "Server is not active"
    exit 1
fi

# Register user and password
echo -ne "\n\nRegistering user $1 with password $2, press enter to continue..."
read press_enter

register=$(curl -s http://127.0.0.1:5000/signup -d '{"username":"'$1'","password":"'$2'"}' -X POST)
output=$(echo $register | jq .access_token 2> /dev/null)

echo -ne "Access token: $output\n"

