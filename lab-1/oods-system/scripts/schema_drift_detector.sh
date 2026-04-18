#!/bin/bash
BASE_COLS=$(duckdb -csv -noheader -c "SELECT string_agg(column_name, ',') FROM (DESCRIBE SELECT * FROM '../providers/satellite_A/observations.csv');")
DRIFT=0

for file in ../providers/*/observations.csv; do
    prov=$(basename $(dirname "$file"))
    CUR_COLS=$(duckdb -csv -noheader -c "SELECT string_agg(column_name, ',') FROM (DESCRIBE SELECT * FROM '$file');")
    
    if [ "$BASE_COLS" != "$CUR_COLS" ]; then
        echo "SCHEMA DRIFT DETECTED:"
        EXTRA=$(duckdb -csv -noheader -c "SELECT column_name FROM (DESCRIBE SELECT * FROM '$file') WHERE column_name NOT IN (SELECT column_name FROM (DESCRIBE SELECT * FROM '../providers/satellite_A/observations.csv'));" 2>/dev/null)
        if [ -n "$EXTRA" ]; then echo "$prov has extra column: $EXTRA"; fi
        DRIFT=1
    fi
done

if [ $DRIFT -eq 0 ]; then echo "SCHEMA STATUS: CONSISTENT"; fi
