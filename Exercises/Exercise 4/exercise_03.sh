#!/bin/bash
# Coding By Rasool Vahdati

# Prompt the user for the name of a file or directory
echo "Enter the name of a file or directory:"
read item

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
