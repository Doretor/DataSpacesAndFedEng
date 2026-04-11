#!/bin/bash
> /tmp/dataset_sizes.txt
for file in ../providers/*/observations.csv; do
    count=$(awk 'END {print NR}' "$file")
    echo "$count $file" >> /tmp/dataset_sizes.txt
done

sort -n /tmp/dataset_sizes.txt -o /tmp/dataset_sizes.txt

smallest=$(head -n 1 /tmp/dataset_sizes.txt)
largest=$(tail -n 1 /tmp/dataset_sizes.txt)

min_val=$(echo "$smallest" | awk '{print $1}')
max_val=$(echo "$largest" | awk '{print $1}')

echo "Smallest dataset: $smallest"
echo "Largest dataset: $largest"
echo "Difference: $((max_val - min_val)) records"
