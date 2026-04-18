#!/bin/bash

# Zabezpieczenie przed brakiem parametru
if [ -z "$1" ]; then
    echo "Usage: ./query_report.sh <OBJECT_ID>"
    exit 1
fi

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="../reports/query_report_${TIMESTAMP}.txt"

echo "DATA SPACE QUERY REPORT" > "$REPORT_FILE"
echo "Generated at: $(date +"%Y-%m-%d %H:%M:%S")" >> "$REPORT_FILE"
echo -e "\n[GLOBAL STATISTICS]" >> "$REPORT_FILE"

# Flaga -csv usuwa wszystkie "ramki" i zostawia sam surowy wynik
TOTAL_OBS=$(duckdb -csv -noheader -c "SELECT COUNT(*) FROM read_csv_auto('../providers/*/observations.csv');")
echo "Total observations: $TOTAL_OBS" >> "$REPORT_FILE"

DISTINCT_OBJ=$(duckdb -csv -noheader -c "SELECT COUNT(DISTINCT object_id) FROM read_csv_auto('../providers/*/observations.csv');")
echo "Distinct objects: $DISTINCT_OBJ" >> "$REPORT_FILE"

echo -e "\n[OBJECT ANALYSIS: $1]" >> "$REPORT_FILE"
echo "Providers containing object:" >> "$REPORT_FILE"

duckdb -csv -noheader -c "SELECT DISTINCT regexp_extract(filename, '.*/(.*?)/observations\.csv', 1) FROM read_csv_auto('../providers/*/observations.csv', filename=true) WHERE object_id = '$1';" >> "$REPORT_FILE"

OBJ_TOTAL=$(duckdb -csv -noheader -c "SELECT COUNT(*) FROM read_csv_auto('../providers/*/observations.csv') WHERE object_id = '$1';")
echo "Total observations: $OBJ_TOTAL" >> "$REPORT_FILE"

echo -e "\n[FEDERATED QUERY COMPARISON]" >> "$REPORT_FILE"
echo "FULL RESULT: $OBJ_TOTAL" >> "$REPORT_FILE"

FED_TOTAL=$(duckdb -csv -noheader -c "SELECT COUNT(*) AS total FROM read_csv_auto(['../providers/satellite_A/observations.csv', '../providers/satellite_B/observations.csv']) WHERE object_id = '$1';" 2>/dev/null)
FED_TOTAL=${FED_TOTAL:-0} 
echo "FEDERATED RESULT: $FED_TOTAL" >> "$REPORT_FILE"

if [ "$OBJ_TOTAL" -eq "$FED_TOTAL" ]; then
    echo "COMPLETE: YES" >> "$REPORT_FILE"
else
    echo "COMPLETE: NO" >> "$REPORT_FILE"
fi

echo -e "\n[SCHEMA VALIDATION]" >> "$REPORT_FILE"
CONSISTENCY="CONSISTENT"
# Dodane awk -F',' aby poprawnie czytać format CSV
BASE_SCHEMA=$(duckdb -csv -noheader -c "DESCRIBE SELECT * FROM '../providers/satellite_A/observations.csv';" | awk -F',' '{print $1, $2}')

for file in ../providers/*/observations.csv; do
    CURRENT_SCHEMA=$(duckdb -csv -noheader -c "DESCRIBE SELECT * FROM '$file';" | awk -F',' '{print $1, $2}')
    if [ "$BASE_SCHEMA" != "$CURRENT_SCHEMA" ]; then
        CONSISTENCY="INCONSISTENT"
        break
    fi
done

echo "Schema consistency: $CONSISTENCY" >> "$REPORT_FILE"
echo "Raport zapisany w: $REPORT_FILE"
