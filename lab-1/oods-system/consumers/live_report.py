import requests
import json
import os
from datetime import datetime
import sys

BROKER_EVENTS_URL = "http://127.0.0.1:7000/events"
TARGET_OBJECT = "OBJ-003"

with open("../contracts/providers_registry.json", "r") as f:
    expected_providers = [p["name"] for p in json.load(f)]

with open("../contracts/event_schema.json", "r") as f:
    contract = json.load(f)
    required_fields = contract["required_fields"]

response = requests.get(BROKER_EVENTS_URL)
events = response.json()

total_events = len(events)
valid_count = 0
invalid_count = 0
active_providers = set()
provider_counts = {}
distinct_objects = set()
obj_target_count = 0

for event in events:
    missing = [field for field in required_fields if field not in event]
    if missing:
        invalid_count += 1
    else:
        valid_count += 1

    prov = event.get("provider")
    if prov:
        active_providers.add(prov)
        provider_counts[prov] = provider_counts.get(prov, 0) + 1

    obj_id = event.get("object_id")
    if obj_id:
        distinct_objects.add(obj_id)
        if obj_id == TARGET_OBJECT:
            obj_target_count += 1

active_providers_sorted = sorted(list(active_providers))
missing_providers = sorted(list(set(expected_providers) - active_providers))
is_complete = "NO" if missing_providers else "YES"

timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

report = f"""REAL-TIME FEDERATION REPORT
---------------------------
Generated at: {timestamp_str}

[STREAM STATUS]
Total events: {total_events}
Valid events: {valid_count}
Invalid events: {invalid_count}

[PROVIDERS]
Active providers:
"""
for p in active_providers_sorted if active_providers_sorted else ["none"]:
    report += f"- {p}\n"

report += "Missing providers:\n"
for p in missing_providers if missing_providers else ["none"]:
    report += f"- {p}\n"

report += "\n[PER-PROVIDER COUNTS]\n"
for p, count in provider_counts.items():
    report += f"{p}: {count}\n"

report += f"""
[OBJECT STATISTICS]
Distinct objects: {len(distinct_objects)}
{TARGET_OBJECT} observations: {obj_target_count}

[FEDERATION STATUS]
COMPLETE: {is_complete}
"""

print(report)

os.makedirs("reports", exist_ok=True)
report_path = f"../reports/stream_report_{file_timestamp}.txt"
with open(report_path, "w") as f:
    f.write(report)

print(f"[INFO] Raport pomyślnie zapisany w pliku: {report_path}")
