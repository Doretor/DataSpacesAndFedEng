import os
import numpy as np

REPORT_FILE = "reports/eo_processing_report.txt"
os.makedirs("reports", exist_ok=True)

ASSET_PATHS = {
    "thumbnail": "assets/thumbnails/thumbnail.jpg",
    "B04": "assets/bands/B04_10m.tif",
    "B08": "assets/bands/B08_10m.tif",
    "NDVI": "results/ndvi/ndvi.npy",
    "NDVI map": "results/ndvi/ndvi_map.png"
}

file_status_lines = []
for name, path in ASSET_PATHS.items():
    if os.path.exists(path):
        file_status_lines.append(f"{name} available")
    else:
        file_status_lines.append(f"{name} missing")

ndvi_min, ndvi_max, ndvi_mean = 0.0, 0.0, 0.0
veg_assessment = "Brak danych o roślinności."

if os.path.exists(ASSET_PATHS["NDVI"]):
    ndvi = np.load(ASSET_PATHS["NDVI"])
    ndvi_min = np.min(ndvi)
    ndvi_max = np.max(ndvi)
    ndvi_mean = np.mean(ndvi)
    
    if ndvi_mean > 0.4:
        veg_assessment = "High vegetation coverage detected."
    elif ndvi_mean > 0:
        veg_assessment = "Moderate vegetation coverage detected."
    else:
        veg_assessment = "Low NDVI - mostly water, clouds, or bare soil."

selected_obs = "Unknown"
final_score = "Unknown"
ranking_file = "reports/observation_ranking.txt"

if os.path.exists(ranking_file):
    with open(ranking_file, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "Recommended observation:" in line:
                if i + 1 < len(lines):
                    selected_obs = lines[i+1].strip()
            if "Final score:" in line and final_score == "Unknown":
                final_score = line.split(":")[1].strip()

report_content = f"""EO PROCESSING REPORT
====================

Selected Observation:
{selected_obs}

Assets:
{chr(10).join(file_status_lines)}

NDVI Statistics:
MIN: {ndvi_min:.2f}
MAX: {ndvi_max:.2f}
MEAN: {ndvi_mean:.2f}

Vegetation Assessment:
{veg_assessment}

Observation Ranking:
FINAL SCORE: {final_score}
"""

with open(REPORT_FILE, "w") as f:
    f.write(report_content)

print("REPORT CREATED")
print(f"{REPORT_FILE}")