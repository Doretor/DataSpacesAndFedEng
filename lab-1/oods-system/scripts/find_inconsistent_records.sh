#!/bin/bash
awk 'FNR>1' ../providers/*/observations.csv | sort | uniq > /tmp/all_unique_records.csv

awk -F',' '{print $2}' /tmp/all_unique_records.csv | sort | uniq -c | awk '$1 > 1 {print $2}' > /tmp/inconsistent_ids.txt

echo "Inconsistencies found for the following objects:"
while read -r id; do
    echo "--- Object: $id ---"
    grep "$id" ../providers/*/observations.csv
done < /tmp/inconsistent_ids.txt
