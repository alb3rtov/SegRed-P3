#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
    echo -ne "Usage: ./all_docs <user> <password>\n"
    exit 1
fi

# Getting token access
echo -ne "\nGetting token access, press enter to continue..."
read press_enter

token=$(curl -s http://myserver.local:5000/login -d '{"username":"'$1'","password":"'$2'"}' -X POST | jq -r .access_token)
echo $token

# Obtaining all the documents from a given user

echo -ne "\nGetting content of json file, press enter to continue..."
read press_enter

curl http://127.0.0.1:5000/$1/_all_docs -H "Authorization: token $token"
