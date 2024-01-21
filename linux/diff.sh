#!/bin/bash

# Check if two file paths are provided as arguments
if [ $# -ne 2 ]; then
  echo "Usage: $0 file1 file2"
  exit 1
fi

file1="$1"
file2="$2"

# Check if both files exist
if [ ! -e "$file1" ]; then
  echo "File '$file1' does not exist."
  exit 1
fi

if [ ! -e "$file2" ]; then
  echo "File '$file2' does not exist."
  exit 1
fi

# Use 'diff' command to compare the files and store the output in a temporary file
temp_diff_file=$(mktemp)
diff "$file1" "$file2" > "$temp_diff_file"

# Print the differences in two columns
awk '
  BEGIN { 
    print "File 1\tFile 2" 
    print "------------------"
  }
  /^</ { 
    printf "%s\t\t%s\n", $2, "" 
  }
  /^>/ { 
    printf "%s\t\t\t%s\n", "", $2 
  }
' "$temp_diff_file"

# Clean up temporary files
rm "$temp_diff_file"
