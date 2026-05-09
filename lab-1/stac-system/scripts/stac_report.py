import json
import os

results_file = "results/federated_results.json"
raw_file = "results/raw_stac_items.json"

if not os.path.exists(results_file) or not os.path.exists(raw_file):
    print("ERROR: First run: federated_search.py")
    exit()

with open(results_file, "r") as f:
    federated_data = json.load(f)

with open(raw_file, "r") as f:
    raw_data = json.load(f)

total_items = len(federated_data)

collections = set([item["collection"] for item in federated_data])

duplicates_removed = len(raw_data) - total_items

failed_queries = 0
empty_regions = 0

all_assets = set()
for item in raw_data:
    if "assets" in item:
        for asset_key in item["assets"].keys():
            all_assets.add(asset_key)

display_assets = []
if "visual" in all_assets or "TCI_10m" in all_assets:
    display_assets.append("visual")
if "product_metadata" in all_assets or "granule_metadata" in all_assets:
    display_assets.append("metadata")
if "thumbnail" in all_assets:
    display_assets.append("thumbnail")

complete_items = 0
for item in federated_data:
    if "id" in item and "datetime" in item and "bbox" in item:
        complete_items += 1

completeness_score = (complete_items / total_items * 100) if total_items > 0 else 0

report_content = f"""STAC REPORT
-----------
Total items: {total_items}
Collections: {', '.join(collections)}
Duplicate items removed: {duplicates_removed}
Failed queries: {failed_queries}
Empty search regions: {empty_regions}
Assets available: {', '.join(display_assets)}
Metadata completeness score: {completeness_score}%
"""

with open("reports/stac_report.txt", "w") as f:
    f.write(report_content)

print(report_content)
