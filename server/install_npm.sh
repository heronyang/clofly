#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Installing $line"
    npm install --no-bin-links -g $line
done < "whitelist-npm-dependencies.txt"
