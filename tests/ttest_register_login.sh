#!/bin/bash

server="https://myserver.local:5000"
curl_options="-s -k"

if [ -z "$1" ] || [ -z "$2" ]; then
    echo -ne "Usage: ./test_register_login.sh <user> <password>"
    exit 1
fi

curl $curl_options $server &> /dev/null

if [ $? -ne 0 ]; then
    echo "Server is not active"
    exit 1
fi

# Trying login with unexistent user
echo -ne "\nTrying logging with user $1 with password $2, press enter to continue..."
read press_enter

login=$(curl $curl_options $server/login -d '{"username":"'$1'","password":"'$2'"}' -X POST)
output=$(echo $login | jq .message 2> /dev/null)

echo -ne "Server response -> Error: $output"

# Register user and password
echo -ne "\n\nRegistering user $1 with password $2, press enter to continue..."
read press_enter

register=$(curl $curl_options $server/signup -d '{"username":"'$1'","password":"'$2'"}' -X POST)
output=$(echo $register | jq .access_token 2> /dev/null)

echo -ne "Server response -> Access token: $output"

# Try to register again with the same user
echo -ne "\n\nTry to register again with the same user, press enter to continue..."
read press_enter

register=$(curl $curl_options $server/signup -d '{"username":"'$1'","password":"'$2'"}' -X POST)
output=$(echo $register | jq .message 2> /dev/null)

echo -ne "Server response -> Error: $output"

# Login with user
echo -ne "\n\nLogging with user $1 with password $2, press enter to continue..."
read press_enter

login=$(curl $curl_options $server/login -d '{"username":"'$1'","password":"'$2'"}' -X POST)
output=$(echo $login | jq .access_token 2> /dev/null)

echo -ne "Server response -> Access token: $output"
