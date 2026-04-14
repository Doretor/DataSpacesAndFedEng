
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="../reports/query_report_${TIMESTAMP}.txt"

echo "DATA SPACE QUERY REPORT" > "$REPORT_FILE"
echo "Generated at: $(date +"%Y%m%d_%H%M%S")" >> "$REPORT_FILE"
echo -e "\n[GLOBAL STATISTICS]" >> "$REPORT_FILE"

TOTAL_OBS=$(duckdb -c "SELECT COUNT(*) FROM read_csv_auto('../providers/*/observations.csv');" -noheader)
echo "Total observations: $TOTAL_OBS" >> "REPORT_FILE"

DISTINCT_OBJ=$(duckdb -c "SELECT COUNT(DISTINCT object_id) FROM read_csv_auto('../providers/*/observations.csv');" -noheader)
echo "Distinct objects: $DISTINCT_OBJ" >> "REPORT_FILE"

echo -e "\n[OBJECT ANALYSIS: $1]" >> "REPORT_FILE"
echo "Providers containing object:" >> "REPORT_FILE"

duckdb -c "SELECT DISTINCT regexp_extract(filename, '.*/(.*?)/observations\.csv', 1) FROM read_csv_auto('../providers/*/observations.csv', filename=true) WHERE object_id = '$1';" -noheader >> "$REPORT_FILE"

OBJ_TOTAL=$(duckdb -c "SELECT COUNT(*) FROM read_csv_auto('../providers/*/observations.csv') WHERE object_id = '$1';" -noheader)
echo "Total observations: $OBJ_TOTAL" >> "REPORT_FILE"

FED_TOTAL=$(duckdb -c "SELECT COUNT(*) AS total FROM read_csv_auto(['../providers/satellite_A/observations.csv', '../providers/satellite_B/observations.csv']) WHERE object_id = '$1';" -noheader)
echo "FEDERATED RESULT: $FED_TOTAL" >> "REPORT_FILE"
