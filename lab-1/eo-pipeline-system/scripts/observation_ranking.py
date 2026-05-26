import os
import requests
from datetime import datetime, timezone

STAC_URL = "https://stac.dataspace.copernicus.eu/v1/search"
QUERY = {
    "collections": ["sentinel-2-l2a"],
    "bbox": [19.0, 50.0, 20.0, 51.0],
    "datetime": "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z",
    "limit": 10
}
REPORT_FILE = "reports/observation_ranking.txt"

os.makedirs("reports", exist_ok=True)

def parse_datetime(value):
    if not value: return None
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value)

def compute_cloud_score(cloud_cover):
    if cloud_cover is None: return 0
    return max(0, 100 - cloud_cover)

def compute_completeness_score(assets_count):
    if assets_count >= 30: return 30
    elif assets_count >= 20: return 20
    elif assets_count >= 10: return 10
    else: return 0

def compute_recency_score(acquisition_time, newest_time):
    if acquisition_time is None or newest_time is None: return 0
    total_days = 30
    age_days = (newest_time - acquisition_time).total_seconds() / 86400
    return max(0, 20 - (age_days / total_days) * 20)

print("Querying STAC...")
response = requests.post(STAC_URL, json=QUERY, timeout=30)
response.raise_for_status()
features = response.json().get("features", [])
print(f"Returned observations: {len(features)}")

if not features:
    print("No observations found. Exiting.")
    exit(0)

observations = []
for item in features:
    props = item.get("properties", {})
    dt_str = props.get("datetime")
    observations.append({
        "id": item.get("id"),
        "datetime_str": dt_str,
        "datetime": parse_datetime(dt_str),
        "cloud_cover": props.get("eo:cloud_cover"),
        "assets_count": len(item.get("assets", {}))
    })

valid_times = [obs["datetime"] for obs in observations if obs["datetime"] is not None]
newest_time = max(valid_times) if valid_times else None

for obs in observations:
    obs["cloud_score"] = compute_cloud_score(obs["cloud_cover"])
    obs["completeness_score"] = compute_completeness_score(obs["assets_count"])
    obs["recency_score"] = compute_recency_score(obs["datetime"], newest_time)
    obs["final_score"] = obs["cloud_score"] + obs["completeness_score"] + obs["recency_score"]

ranked = sorted(observations, key=lambda x: x["final_score"], reverse=True)

report_lines = ["OBSERVATION RANKING ENGINE", "=" * 60]
for idx, obs in enumerate(ranked, 1):
    report_lines.append(f"{idx}. {obs['id']}")
    report_lines.append(f"   Time: {obs['datetime_str']}")
    report_lines.append(f"   Cloud cover: {obs['cloud_cover']}")
    report_lines.append(f"   Assets count: {obs['assets_count']}")
    report_lines.append(f"   Cloud score: {obs['cloud_score']:.2f}")
    report_lines.append(f"   Completeness score: {obs['completeness_score']:.2f}")
    report_lines.append(f"   Recency score: {obs['recency_score']:.2f}")
    report_lines.append(f"   Final score: {obs['final_score']:.2f}")
    report_lines.append("-" * 30)

report_lines.append(f"\nRecommended observation:\n{ranked[0]['id']}")

with open(REPORT_FILE, "w") as f:
    f.write("\n".join(report_lines))

print(f"Ranking report saved to {REPORT_FILE}")