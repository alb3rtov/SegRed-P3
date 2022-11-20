#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
    echo -ne "Usage: ./test_register_login.sh <user> <password>\n"
    exit 1
fi

# Register user and password
echo -ne "\n\nRegistering user $1 with password $2, press enter to continue..."
read press_enter

register=$(curl -s "https://myserver.local:5000"/signup -d '{username:"'$1'","password":"'$2'"}' -X POST)
output=$(echo $register)

echo -ne "Access token: $output\n"

