#!/bin/bash
duckdb -csv -noheader -c "
SELECT object_id || ' inconsistency detected (temperature):' || chr(10) || 
       string_agg(regexp_extract(filename, '.*/(.*?)/observations\.csv', 1) || ': ' || temperature, chr(10))
FROM read_csv_auto('../providers/*/observations.csv', filename=true)
GROUP BY object_id HAVING MAX(temperature) - MIN(temperature) > 0.5;"
