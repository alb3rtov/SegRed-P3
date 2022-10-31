#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo -ne "Usage: ./test_register_login.sh <user> <password> <doc_id>"
    exit 1
fi

curl -s http://127.0.0.1:5000/ &> /dev/null

if [ $? -ne 0 ]; then
    echo "Server is not active"
    exit 1
fi

# Getting token access
echo -ne "\nGetting token access, press enter to continue..."
read press_enter

token=$(curl -s http://127.0.0.1:5000/login -d '{"username":"'$1'","password":"'$2'"}' -X POST | jq -r .access_token)
echo $token

# Create new json file
echo -ne "\nCreating new json file, press enter to continue..."
read press_enter

curl http://127.0.0.1:5000/$1/$3 -H "Authorization: token $token" -d '{"doc_content": {"fruit": "Apple", "size": "Large", "color": "Red"}}' -X POST

# Get content of json file
echo -ne "\nGetting content of json file, press enter to continue..."
read press_enter

curl http://127.0.0.1:5000/$1/$3 -H "Authorization: token $token"

# Modify json file
echo -ne "\nModify json file, press enter to continue..."
read press_enter

curl http://127.0.0.1:5000/$1/$3 -H "Authorization: token $token" -d '{"doc_content": {"fruit": "Apple", "size": "Small", "color": "Green"}}' -X PUT

# Delete json file
echo -ne "\nDeleting json file, press enter to continue..."
read press_enter

curl http://127.0.0.1:5000/$1/$3 -H "Authorization: token $token" -X DELETE