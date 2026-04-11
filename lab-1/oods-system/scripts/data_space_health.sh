#!/bin/bash

REPORT_FILE="../reports/data_space_health.txt"

total_datasets=$(ls ../providers/*/observations.csv 2>/dev/null | wc -l)

missing_metadata_count=0
for file in ../providers/*/observations.csv; do
    clean_path="${file#../}"
    if ! grep -q "$clean_path" ../metadata_catalog/*.json 2>/dev/null; then
        missing_metadata_count=$((missing_metadata_count + 1))
    fi
done

empty_datasets=$(find ../providers/ -name "observations.csv" -size 0 | wc -l)

inconsistent_datasets=0
paths_from_metadata=$(grep -h -o "providers/[^\"]*observations.csv" ../metadata_catalog/*.json 2>/dev/null)
for dataset_path in $paths_from_metadata; do
    actual_path="../$dataset_path"
    if [ ! -f "$actual_path" ]; then
        inconsistent_datasets=$((inconsistent_datasets + 1))
    fi
done

dist_count=$(cat ../providers/*/observations.csv 2>/dev/null | grep "OBJ-003" | wc -l)
fed_count=0
for dataset_path in $paths_from_metadata; do
    actual_path="../$dataset_path"
    if [ -f "$actual_path" ]; then 
        fed_count=$((fed_count + $(grep -c "OBJ-003" "$actual_path")))
    fi
done

completeness="NO"
if [ "$dist_count" -eq "$fed_count" ]; then completeness="YES"; fi

cat <<EOF > "$REPORT_FILE"
DATA SPACE HEALTH REPORT
Total datasets: $total_datasets
Datasets missing metadata: $missing_metadata_count
Empty datasets: $empty_datasets
Inconsistent metadata entries: $inconsistent_datasets
Federated queries complete: $completeness
EOF
