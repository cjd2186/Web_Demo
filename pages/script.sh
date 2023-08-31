#!/bin/bash

# Assuming the text file is named "filenames.txt"
input_file="files.txt"

# Read each line from the input file
while IFS= read -r filename; do
    # Create a new Python file with the filename
    touch "${filename}.py"
    echo "print('Hello from ${filename}.py')" > "${filename}.py"
done < "$input_file"

