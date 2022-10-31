#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
    echo -ne "Usage: ./test_register_login.sh <user> <password>"
    exit 1
fi

curl -s http://127.0.0.1:5000/ &> /dev/null

if [ $? -ne 0 ]; then
    echo "Server is not active"
    exit 1
fi

# Trying login with unexistent user
echo -ne "\nTrying logging with user $1 with password $2, press enter to continue..."
read press_enter

login=$(curl -s http://127.0.0.1:5000/login -d '{"username":"'$1'","password":"'$2'"}' -X POST)
output=$(echo $login | jq .message 2> /dev/null)

echo -ne "Error: $output"

# Register user and password
echo -ne "\n\nRegistering user $1 with password $2, press enter to continue..."
read press_enter

register=$(curl -s http://127.0.0.1:5000/signup -d '{"username":"'$1'","password":"'$2'"}' -X POST)
output=$(echo $register | jq .access_token 2> /dev/null)

echo -ne "Access token: $output"

# Try to register again with the same user
echo -ne "\n\nTry to register again with the same user, press enter to continue..."
read press_enter

register=$(curl -s http://127.0.0.1:5000/signup -d '{"username":"'$1'","password":"'$2'"}' -X POST)
output=$(echo $register | jq .message 2> /dev/null)

echo -ne "Error: $output"

# Login with user
echo -ne "\n\nLogging with user $1 with password $2, press enter to continue..."
read press_enter

login=$(curl -s http://127.0.0.1:5000/login -d '{"username":"'$1'","password":"'$2'"}' -X POST)
output=$(echo $login | jq .access_token 2> /dev/null)

echo -ne "Access token: $output"