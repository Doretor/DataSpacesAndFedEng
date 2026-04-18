#!/bin/bash
FULL=$(duckdb -csv -noheader -c "SELECT COUNT(*) FROM read_csv_auto('../providers/*/observations.csv');")
FED=$(duckdb -csv -noheader -c "SELECT COUNT(*) FROM read_csv_auto(['../providers/satellite_A/observations.csv', '../providers/satellite_B/observations.csv']);" 2>/dev/null)

if [ "$FULL" -eq "${FED:-0}" ]; then
    echo "FEDERATED RESULT: COMPLETE"
else
    echo "FEDERATED RESULT: INCOMPLETE"
    echo "MISSING PROVIDERS: ground_station"
fi
