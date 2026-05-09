import requests
import os

os.makedirs("reports", exist_ok=True)
url = "https://stac.dataspace.copernicus.eu/v1/search"

scenarios = [
    {"name": "WILDFIRE REGION", "bbox": [13.0, 37.0, 18.0, 41.0]},
    {"name": "FLOOD REGION", "bbox": [18.5, 49.5, 21.5, 51.0]},
    {"name": "VOLCANIC REGION", "bbox": [14.5, 37.4, 15.4, 38.1]}
]

report_lines = [
    "EMERGENCY MONITORING REPORT",
    "---------------------------",
    "Time window: 2024-07-01/2024-07-31",
    "Collection: sentinel-2-l2a",
    "Cloud cover threshold: < 30%\n"
]

for s in scenarios:
    query = {
        "collections": ["sentinel-2-l2a"],
        "datetime": "2024-07-01T00:00:00Z/2024-07-31T23:59:59Z",
        "bbox": s["bbox"],
        "query": {"eo:cloud_cover": {"lt": 30}},
        "limit": 10
    }
    
    try:
        resp = requests.post(url, json=query, timeout=20)
        resp.raise_for_status()
        items = resp.json().get("features", [])
        
        report_lines.append(f"[{s['name']}]")
        report_lines.append(f"Returned products: {len(items)}")
        report_lines.append("Example products:")
        
        for item in items[:3]:
            report_lines.append(f"- {item['id']}")
        report_lines.append("")
        
    except Exception as e:
        report_lines.append(f"[{s['name']}] Błąd: {e}\n")

report_content = "\n".join(report_lines)
with open("reports/emergency_monitoring_report.txt", "w") as f:
    f.write(report_content)

