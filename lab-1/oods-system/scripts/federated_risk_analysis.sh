#!/bin/bash
FULL=$(duckdb -csv -noheader -c "SELECT COUNT(*) FROM read_csv_auto('../providers/*/observations.csv');")
FED=$(duckdb -csv -noheader -c "SELECT COUNT(*) FROM read_csv_auto(['../providers/satellite_A/observations.csv', '../providers/satellite_B/observations.csv']);" 2>/dev/null)
FED=${FED:-0}
MISSING=$((FULL - FED))
LOSS=$(echo "scale=1; $MISSING * 100 / $FULL" | bc)

echo "FULL: $FULL"
echo "FEDERATED: $FED"
echo "MISSING: $MISSING"
echo "LOSS: ${LOSS}%"
