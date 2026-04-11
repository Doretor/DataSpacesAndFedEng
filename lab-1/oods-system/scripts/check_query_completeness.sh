#!/bin/bash
OBJ_ID=$1

dist_count=$(cat ../providers/*/observations.csv | grep "$OBJ_ID" | wc -l)
fed_count=0

paths_from_metadata=$(grep -h -o "providers/[^\"]*observations.csv" ../metadata_catalog/*.json 2>/dev/null)

for dataset_path in $paths_from_metadata; do
    actual_path="../$dataset_path"
    if [ -f "$actual_path" ]; then
        matches=$(grep -c "$OBJ_ID" "$actual_path")
        fed_count=$((fed_count + matches))
    fi
done

echo "Distributed search found: $dist_count results"
echo "Federated search found: $fed_count results"

if [ "$dist_count" -eq "$fed_count" ]; then
    echo "Conclusion: Federated access returns COMPLETE results."
else
    echo "Conclusion: Federated access returns INCOMPLETE results."
fi
