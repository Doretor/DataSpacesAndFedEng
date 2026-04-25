SELECT 'satellite_A' AS provider, * FROM read_json_auto('http://127.0.0.1:8001/observations')
UNION ALL
SELECT 'satellite_B' AS provider, * FROM read_json_auto('http://127.0.0.1:8002/observations')
UNION ALL
SELECT 'ground_station' AS provider, * FROM read_json_auto('http://127.0.0.1:8003/observations');
