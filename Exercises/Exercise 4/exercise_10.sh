#!/bin/bash
# Coding By Rasool Vahdati

# How to error occur?
# Answer: The error occurred because the mkdir command was used to create a directory named learning, but a directory or file with that name already exists in the current location. mkdir cannot create when folder exists.


# fix
if [ ! -d "learning" ]; then
    # Create the directory if it does not exist
    mkdir learning
    echo "Directory 'learning' created."
else
    echo "Directory 'learning' already exists."
fi
