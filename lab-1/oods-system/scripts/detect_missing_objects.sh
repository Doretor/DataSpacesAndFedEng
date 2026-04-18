#!/bin/bash
duckdb -c "
SELECT (object_id || ' missing in: ' || array_to_string(list_filter(['satellite_A', 'satellite_B', 'ground_station'], p -> NOT list_contains(providers, p)), ', ')) AS 'Missing objects'
FROM (
    SELECT object_id, list(DISTINCT regexp_extract(filename, '.*/(.*?)/observations\.csv', 1)) as providers
    FROM read_csv_auto('../providers/*/observations.csv', filename=true)
    GROUP BY object_id
) WHERE length(providers) < 3;" -noheader
