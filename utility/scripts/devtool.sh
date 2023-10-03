#!/bin/bash

# Check whether devtool.json exists in main folder
if [ -f ./devtool.json ]; then
   rm -f ./devtool.json
fi

echo "{
  \"images\": [
    {
      \"path\": \"$PWD\",
      \"tag\": \"utility\"
    }
  ]
}" > ./devtool.json

# Check whether command `jls-devtool` available
if ! command -v jls-devtool &> /dev/null
then
    echo "jls-devtool could not be found"
    exit
fi

jls-devtool -iu $PWD/devtool.json
