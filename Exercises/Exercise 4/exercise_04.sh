#!/bin/bash
# Coding By Rasool Vahdati

# Check if an argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <file_or_directory_name>"
    exit 1
fi

item="$1"

# Check if the item exists
if [ -e "$item" ]; then
    # Check if it is a regular file
    if [ -f "$item" ]; then
        echo "$item is a regular file."
    # Check if it is a directory
    elif [ -d "$item" ]; then
        echo "$item is a directory."
    # If it is neither a regular file nor a directory
    else
        echo "$item is another type of file."
    fi

    # Perform ls command with long listing option
    ls -l "$item"
else
    echo "$item does not exist."
fi
