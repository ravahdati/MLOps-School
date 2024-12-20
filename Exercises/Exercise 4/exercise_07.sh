#!/bin/bash
# Coding By Rasool Vahdati

# Define the function
file_count() {
    local count=$(find . -maxdepth 1 -type f | wc -l)
    echo "The number of files in the current directory is: $count"
}

# Call the function
file_count
