#!/bin/bash

i=0

server="https://myserver.local:5000"

if [ -z "$1" ] || [ -z "$2" ]; then
    echo -ne "Usage: ./test_register_login.sh <user> <password>\n"
    exit 1
fi

# Getting token access
echo -ne "\nGetting token access, press enter to continue..."
read press_enter

token=$(curl -s $server/login -d '{"username":"'$1'","password":"'$2'"}' -X POST | jq -r .access_token)
echo $token

if [[ $token == 'null' ]]; then
    echo "Error in user or password"
    exit 1
fi

echo -ne "\nCreating new json files with name from 0 to 4, press enter to continue..."
read press_enter

while [ $i -lt 5 ]
do
    curl $server/$1/$i -H "Authorization: token $token" -d '{"doc_content": {"fruit": "Apple", "size": "Large", "color": "Red"}}' -X POST
    ((i++))
done

# Obtaining all the documents from a given user

echo -ne "\nGetting content of json file, press enter to continue..."
read press_enter

curl $server/$1/_all_docs -H "Authorization: token $token"
