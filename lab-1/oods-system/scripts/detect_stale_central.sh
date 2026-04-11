#!/bin/bash

for prov_file in ../providers/*/observations.csv; do
    provider=$(basename $(dirname "$prov_file"))

    central_file="../central_repository/observations_${provider}.csv"

    if [ -f "$central_file" ]; then
        if ! cmp -s "$prov_file" "$central_file"; then
            echo "STALE DATA: Central repository is outdated for $provider"
        fi
    else
        echo "MISSING COPY: No central copy found for $provider"
    fi
done
