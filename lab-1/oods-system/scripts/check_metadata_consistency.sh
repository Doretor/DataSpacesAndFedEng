#!/bin/bash

paths_from_metadata=$(grep -h -o "providers/[^\"]*observations.csv" ../metadata_catalog/*.json 2>/dev/null)

for dataset_path in $paths_from_metadata; do
    actual_path="../$dataset_path"

    if [ ! -f "$actual_path" ]; then
        echo "Inconsistent: Metadata references non-existing dataset -> $dataset_path"
    elif [ ! -s "$actual_path" ]; then
        echo "Inconsistent: Metadata references empty dataset -> $dataset_path"
    fi
done
