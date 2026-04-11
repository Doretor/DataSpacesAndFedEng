#!/bin/bash

for file in ../providers/*/observations.csv; do
    clean_path="${file#../}"
    if ! grep -q "$clean_path" ../metadata_catalog/*.json 2>/dev/null; then
        echo "Missing metadata entry for dataset: $clean_path"
    fi
done
