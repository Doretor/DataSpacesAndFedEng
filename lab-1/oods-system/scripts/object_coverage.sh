#!/bin/bash

> /tmp/provider_objects.txt
for file in ../providers/*/observations.csv; do
    awk -F',' 'FNR>1 {print $2}' "$file" | sort | uniq >> /tmp/provider_objects.txt
done

total_providers=$(ls -d ../providers/*/ | wc -l)
sort /tmp/provider_objects.txt | uniq -c > /tmp/object_counts.txt

echo "Objects present in ALL providers:"
awk -v t="$total_providers" '$1 == t {print $2}' /tmp/object_counts.txt

echo -e "\nObjects present in ONLY ONE provider:"
awk '$1 == 1 {print $2}' /tmp/object_counts.txt
