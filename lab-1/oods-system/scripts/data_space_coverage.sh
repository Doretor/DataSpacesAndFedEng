#!/bin/bash
duckdb -csv -noheader -c "
WITH provider_counts AS (
    SELECT object_id, COUNT(DISTINCT regexp_extract(filename, '.*/(.*?)/observations\.csv', 1)) as p_count
    FROM read_csv_auto('../providers/*/observations.csv', filename=true)
    GROUP BY object_id
),
stats AS (
    SELECT COUNT(*) as total, SUM(CASE WHEN p_count = 3 THEN 1 ELSE 0 END) as full_cov, SUM(CASE WHEN p_count < 3 THEN 1 ELSE 0 END) as partial
    FROM provider_counts
)
SELECT 'TOTAL OBJECTS: ' || total || chr(10) || 'FULL COVERAGE: ' || full_cov || chr(10) || 'PARTIAL: ' || partial || chr(10) || 'COVERAGE SCORE: ' || ROUND(full_cov * 100.0 / total, 0) || '%'
FROM stats;"
