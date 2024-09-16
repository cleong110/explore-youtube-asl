#!/bin/bash
# given a list of language codes pulled from YouTube ASL 25's CSV, count how many there are of each and sort. 
# Probably easier to do in numpy :wq

# Enable strict mode for safer script execution
set -euo pipefail

# Check for correct number of arguments
if [[ $# -lt 2 || $# -gt 3 ]]; then
    echo "Usage: $0 <file1> <file2> [--sort]"
    exit 1
fi

# File paths from arguments
file1="$1"
file2="$2"
sort_output=false

# Check if the optional --sort flag is present
if [[ $# -eq 3 && "$3" == "--sort" ]]; then
    sort_output=true
fi

# Function to count occurrences
count_occurrences() {
    local string="$1"
    count=$(grep -w -o "$string" "$file2" | wc -l || true)
    echo "$string, $count"
}

export -f count_occurrences
export file2

# Collect the output into a variable
output=$(parallel --line-buffer --colsep '\n' count_occurrences :::: "$file1")

# If --sort option is provided, sort by the second column (numeric sort)
if [[ "$sort_output" == true ]]; then
    echo "$output" | sort -t ',' -k2,2n
else
    echo "$output"
fi

