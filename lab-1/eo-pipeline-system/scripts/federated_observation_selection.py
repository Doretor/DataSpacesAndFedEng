import os
import requests

STAC_URL = "https://stac.dataspace.copernicus.eu/v1/search"
AOI = [19.0, 50.0, 20.0, 51.0]
TIME_WINDOW = "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z"
REPORT_FILE = "reports/federated_observation_selection.txt"

os.makedirs("reports", exist_ok=True)

QUERIES = {
    "Sentinel-2 Optical": {
        "collections": ["sentinel-2-l2a"],
        "bbox": AOI,
        "datetime": TIME_WINDOW,
        "limit": 5
    },
    "Sentinel-1 SAR": {
        "collections": ["sentinel-1-grd"],
        "bbox": AOI,
        "datetime": TIME_WINDOW,
        "limit": 5
    }
}

def query_stac(query):
    response = requests.post(STAC_URL, json=query, timeout=30)
    response.raise_for_status()
    return response.json().get("features", [])

def summarize_item(item):
    properties = item.get("properties", {})
    assets = item.get("assets", {})
    return {
        "id": item.get("id"),
        "datetime": properties.get("datetime"),
        "cloud_cover": properties.get("eo:cloud_cover"),
        "assets_count": len(assets),
        "platform": properties.get("platform"),
        "constellation": properties.get("constellation"),
        "instrument": properties.get("instruments")
    }

def compute_sensor_score(sensor_name, items, scenario):
    if not items:
        return 0
    
    score = min(len(items), 5) * 10
    
    if sensor_name == "Sentinel-2 Optical":
        clouds = [i["cloud_cover"] for i in items if i["cloud_cover"] is not None]
        avg_cloud = sum(clouds) / len(clouds) if clouds else 50
        
        if scenario == "normal":
            score += (100 - avg_cloud)
        elif scenario == "cloudy":
            score -= 50
        elif scenario == "night":
            score -= 100

    elif sensor_name == "Sentinel-1 SAR":
        if scenario == "normal":
            score += 50
        elif scenario == "cloudy":
            score += 80
        elif scenario == "night":
            score += 80

    return max(0, score)

print("FEDERATED OBSERVATION SELECTION")
print("============================================================")

summaries = {}

for sensor_name, query in QUERIES.items():
    print(f"Querying: {sensor_name}")
    features = query_stac(query)
    print(f"{sensor_name} products: {len(features)}")
    summaries[sensor_name] = [summarize_item(item) for item in features]

scenarios = ["normal", "cloudy", "night"]
report_lines = ["FEDERATED OBSERVATION SELECTION REPORT", "======================================", "Sensors compared:", "- Sentinel-2 Optical", "- Sentinel-1 SAR", "", "Scenario-based sensor selection:", "--------------------------------"]

for scenario in scenarios:
    best_sensor = None
    best_score = -1
    scenario_scores = []
    
    for sensor_name, items in summaries.items():
        score = compute_sensor_score(sensor_name, items, scenario)
        scenario_scores.append((sensor_name, score))
        if score > best_score:
            best_score = score
            best_sensor = sensor_name
            
    report_lines.append(f"Scenario: {scenario}")
    report_lines.append(f"Recommended sensor: {best_sensor}")
    report_lines.append("Scores:")
    for sensor, score in scenario_scores:
        report_lines.append(f"- {sensor}: {score:.2f}")
    report_lines.append("")

with open(REPORT_FILE, "w") as f:
    f.write("\n".join(report_lines))

print("\nFEDERATED SELECTION COMPLETE")
print(f"REPORT SAVED TO: {REPORT_FILE}")