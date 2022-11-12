#!/bin/bash

server="https://myserver.local:5000"

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo -ne "Usage: ./test_register_login.sh <user> <password> <doc_id>"
    exit 1
fi

curl -s $server &> /dev/null

if [ $? -ne 0 ]; then
    echo "Server is not active"
    exit 1
fi

# Getting token access
echo -ne "\nGetting token access, press enter to continue..."
read press_enter

token=$(curl -s $server/login -d '{"username":"'$1'","password":"'$2'"}' -X POST | jq -r .access_token)
echo $token

if [[ $token == 'null' ]]; then
    echo "Error: user or password incorrect\n"
    exit 1
fi

# Create new json file
echo -ne "\nCreating new json file, press enter to continue..."
read press_enter

curl $server/$1/$3 -H "Authorization: token $token" -d '{"doc_content": {"fruit": "Apple", "size": "Large", "color": "Red"}}' -X POST

# Get content of json file
echo -ne "\nGetting content of json file, press enter to continue..."
read press_enter

curl $server/$1/$3 -H "Authorization: token $token"

# Modify json file
echo -ne "\nModify json file, press enter to continue..."
read press_enter

curl $server/$1/$3 -H "Authorization: token $token" -d '{"doc_content": {"fruit": "Apple", "size": "Small", "color": "Green", "flavour": "Bad"}}' -X PUT

# Get content of json file
echo -ne "\nGetting content of json file, press enter to continue..."
read press_enter

curl $server/$1/$3 -H "Authorization: token $token"

# Delete json file
echo -ne "\nDeleting json file, press enter to continue..."
read press_enter

curl $server/$1/$3 -H "Authorization: token $token" -X DELETE
