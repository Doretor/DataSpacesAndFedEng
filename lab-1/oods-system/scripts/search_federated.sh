#!/bin/bash

ID=$1
WYN=0

for file in ../metadata_catalog/*.json
do
        echo "$(grep "data_path" $file | cut -d '"' -f4 | cut -d '/' -f2): $(grep "$1" ../$(grep "data_path" $file | cut -d '"' -f4) | wc -l)"

done

echo "In all datasets: $(cat $(grep "data_path" ../metadata_catalog/*.json | cut -d '"' -f4 | sed 's/^/..\//') | grep "$ID" | wc -l)"

