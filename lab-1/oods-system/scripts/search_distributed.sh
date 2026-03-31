#!/bin/bash

ID=$1

for file in ../providers/*/observations.csv
do
        echo "$(dirname $file | cut -d '/' -f3): $(grep "$ID" $file | wc -l)"

done

echo "In all datasets: $(cat ../providers/*/observations.csv | grep "$ID" | wc -l)"
