import json
from datetime import datetime
import os

results_file = "results/federated_results.json"

if not os.path.exists(results_file):
    print(f"Błąd: Nie znaleziono pliku {results_file}. Uruchom najpierw Task 8.")
    exit()

with open(results_file, "r") as f:
    data = json.load(f)

dates = []
for item in data:
    dt_str = item["datetime"].replace('Z', '+00:00')
    dates.append(datetime.fromisoformat(dt_str))

dates.sort()
earliest = dates[0]
latest = dates[-1]
span = latest - earliest

gaps = 0
for i in range(1, len(dates)):
    diff = dates[i] - dates[i-1]
    if diff.days >= 1:
        gaps += 1

report = f"""P2: TEMPORAL COVERAGE ANALYSIS

1. Earliest observation: {earliest.isoformat()}
2. Latest observation: {latest.isoformat()}
3. Total observation span: {span.days} days and {span.seconds // 3600} hours
4. Temporal gaps found: {gaps} gaps longer than 24 hours.
"""

with open("reports/temporal_analysis.txt", "w") as f:
    f.write(report)
