#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
    echo -ne "Usage: ./test_register_login.sh <user> <password>"
    exit 1
fi


# Login with user
echo -ne "\n\nLogging with user $1 with password $2, press enter to continue..."
read press_enter

login=$(curl -s "https://myserver.local:5000"/login -d '{"username":"'$1'","password":"'$2'"}' -X POST)
output=$(echo $login | jq .access_token 2> /dev/null)

echo -ne "Access token: $output\n"
