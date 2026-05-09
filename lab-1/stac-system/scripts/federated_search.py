import requests
import json
import os

os.makedirs("results", exist_ok=True)
os.makedirs("reports", exist_ok=True)

url = "https://stac.dataspace.copernicus.eu/v1/search"

queries = [
    {
        "name": "Query 1: Optical monitoring of southern Poland",
        "payload": {
            "collections": ["sentinel-2-l2a"],
            "bbox": [19.0, 50.0, 20.0, 51.0],
            "datetime": "2024-01-01T00:00:00Z/2024-01-10T23:59:59Z",
            "limit": 10
        }
    },
    {
        "name": "Query 2: Optical monitoring of Baltic region",
        "payload": {
            "collections": ["sentinel-2-l2a"],
            "bbox": [17.0, 54.0, 19.0, 55.5],
            "datetime": "2024-01-01T00:00:00Z/2024-01-10T23:59:59Z",
            "limit": 10
        }
    },
    {
        "name": "Query 3: Radar monitoring of southern Poland",
        "payload": {
            "collections": ["sentinel-1-grd"],
            "bbox": [19.0, 50.0, 20.0, 51.0],
            "datetime": "2024-01-01T00:00:00Z/2024-01-10T23:59:59Z",
            "limit": 10
        }
    }
]

raw_items = []
unified_catalog = []
seen_ids = set()
duplicates_removed = 0
query_results_count = {}

for q in queries:
    try:
        response = requests.post(url, json=q["payload"], timeout=20)
        response.raise_for_status()
        data = response.json()
        
        items = data.get("features", [])
        query_results_count[q["name"]] = len(items)
        
        for item in items:
            raw_items.append(item)
            item_id = item["id"]
            
            if item_id in seen_ids:
                duplicates_removed += 1
                continue
                
            seen_ids.add(item_id)
            
            unified_item = {
                "id": item_id,
                "collection": item.get("collection", "unknown"),
                "datetime": item["properties"]["datetime"],
                "bbox": item.get("bbox", []),
                "assets_count": len(item.get("assets", {})),
                "source_provider": "CDSE",
                "source_query": q["name"]
            }
            unified_catalog.append(unified_item)
            
    except Exception as e:
        print(f"Błąd dla {q['name']}: {e}")

unified_catalog.sort(key=lambda x: x["datetime"])

with open("results/raw_stac_items.json", "w") as f:
    json.dump(raw_items, f, indent=2)

with open("results/federated_results.json", "w") as f:
    json.dump(unified_catalog, f, indent=2)

total_unique = len(unified_catalog)
earliest = unified_catalog[0]["datetime"] if total_unique > 0 else "N/A"
latest = unified_catalog[-1]["datetime"] if total_unique > 0 else "N/A"
collections_used = list(set([i["collection"] for i in unified_catalog]))

with open("reports/federation_summary.txt", "w") as f:
    f.write("FEDERATION SUMMARY REPORT\n")
    for name, count in query_results_count.items():
        f.write(f"- {name}: {count} products\n")
    
    f.write(f"\n- Number of duplicates removed: {duplicates_removed}\n")
    f.write(f"- Total number of unique products: {total_unique}\n")
    f.write(f"- Earliest observation: {earliest}\n")
    f.write(f"- Latest observation: {latest}\n")
    f.write(f"- Collections represented: {', '.join(collections_used)}\n\n")
