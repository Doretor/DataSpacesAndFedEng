#!/bin/bash
duckdb -csv -noheader -c "
WITH total AS (SELECT COUNT(*) as t FROM read_csv_auto('../providers/*/observations.csv'))
SELECT regexp_extract(filename, '.*/(.*?)/observations\.csv', 1) || ': ' || COUNT(*) || ' (' || ROUND(COUNT(*) * 100.0 / MAX(t.t), 0) || '%)'
FROM read_csv_auto('../providers/*/observations.csv', filename=true), total t
GROUP BY filename ORDER BY COUNT(*) DESC;"

DOMINANT=$(duckdb -csv -noheader -c "SELECT regexp_extract(filename, '.*/(.*?)/observations\.csv', 1) FROM read_csv_auto('../providers/*/observations.csv', filename=true) GROUP BY filename ORDER BY COUNT(*) DESC LIMIT 1;")
echo "DOMINANT PROVIDER: $DOMINANT"
