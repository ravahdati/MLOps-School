#!/bin/bash
# Coding By Rasool Vahdati

# Initialize line number counter
line_number=1

# Loop through each line in the /etc/passwd file
for line in $(cat /etc/passwd); do
    # Print the line number followed by a colon and a space, then the line
    echo "$line_number: $line"
    # Increment the line number counter
    ((line_number++))
done
