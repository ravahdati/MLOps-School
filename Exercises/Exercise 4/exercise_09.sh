#!/bin/bash
# Coding By Rasool Vahdati

# Enable nullglob to handle cases where there are no .jpg files
shopt -s nullglob

# Get today's date
today=$(date +"%Y%m%d")

# get all file with *.jpg and rename it
for file in *.jpg; do
    new_name="${today}${file}"
    mv "$file" "$new_name"
    echo "Renamed '$file' to '$new_name'"
done

# Disable nullglob after use
shopt -u nullglob

# Check if any files were renamed
if [ "$(ls *.jpg 2>/dev/null)" == "" ]; then
    echo "No .jpg files found in the current directory."
fi
