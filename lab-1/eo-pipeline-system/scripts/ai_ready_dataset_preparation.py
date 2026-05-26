import os
import json
import shutil

DATASET_DIR = "dataset"
IMAGES_DIR = "dataset/images"
METADATA_DIR = "dataset/metadata"

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

FILES_TO_INCLUDE = {
    "ndvi_map": "results/ndvi/ndvi_map.png",
    "water_mask": "results/ndvi/water_mask.png",
    "observation_low_cloud": "results/ndvi_comparison/low_cloud_observation_ndvi_map.png",
    "observation_high_cloud": "results/ndvi_comparison/high_cloud_observation_ndvi_map.png",
    "time_series_trend": "results/ndvi_timeseries/mean_ndvi_trend.png"
}

QUALITY_RULES = {
    "excellent": {"max_cloud_cover": 10, "min_ndvi": 0.5},
    "good": {"max_cloud_cover": 30, "min_ndvi": 0.3},
    "limited": {"max_cloud_cover": 70, "min_ndvi": 0.1}
}

def determine_quality(cloud_cover, mean_ndvi):
    if cloud_cover <= QUALITY_RULES["excellent"]["max_cloud_cover"] and mean_ndvi >= QUALITY_RULES["excellent"]["min_ndvi"]:
        return "excellent", "AI_READY"
    elif cloud_cover <= QUALITY_RULES["good"]["max_cloud_cover"] and mean_ndvi >= QUALITY_RULES["good"]["min_ndvi"]:
        return "good", "AI_READY"
    elif cloud_cover <= QUALITY_RULES["limited"]["max_cloud_cover"] and mean_ndvi >= QUALITY_RULES["limited"]["min_ndvi"]:
        return "limited", "NEEDS_FILTERING"
    else:
        return "poor", "NOT_SUITABLE"

synthetic_observations = [
    {"id": "OBS_001", "cloud_cover": 5, "mean_ndvi": 0.62, "sensor": "Sentinel-2"},
    {"id": "OBS_002", "cloud_cover": 18, "mean_ndvi": 0.44, "sensor": "Sentinel-2"},
    {"id": "OBS_003", "cloud_cover": 68, "mean_ndvi": 0.21, "sensor": "Sentinel-2"}
]

print("AI-READY EO DATASET PREPARATION")
print("============================================================")

copied_assets = []
for key, path in FILES_TO_INCLUDE.items():
    if os.path.exists(path):
        filename = os.path.basename(path)
        dest = os.path.join(IMAGES_DIR, filename)
        shutil.copy(path, dest)
        copied_assets.append(dest)
        print(f"COPIED: {dest}")
    else:
        print(f"MISSING: {path}")

quality_counts = {"excellent": 0, "good": 0, "limited": 0, "poor": 0}

for obs in synthetic_observations:
    quality, suitability = determine_quality(obs["cloud_cover"], obs["mean_ndvi"])
    quality_counts[quality] += 1
        
    metadata = {
        "observation_id": obs["id"],
        "sensor": obs["sensor"],
        "cloud_cover": obs["cloud_cover"],
        "mean_ndvi": obs["mean_ndvi"],
        "quality": quality,
        "suitability": suitability,
        "selected_assets": copied_assets,
        "labels": {
            "vegetation_monitoring": suitability,
            "ai_training": suitability,
            "cloud_conditions": "LOW" if obs["cloud_cover"] < 20 else "HIGH"
        }
    }
    
    meta_path = os.path.join(METADATA_DIR, f"{obs['id']}.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"METADATA CREATED: {meta_path}")

summary = {
    "dataset_size": len(synthetic_observations),
    "images_directory": IMAGES_DIR,
    "metadata_directory": METADATA_DIR,
    "quality_distribution": {k: v for k, v in quality_counts.items() if v > 0}
}

with open(os.path.join(METADATA_DIR, "dataset_summary.json"), "w") as f:
    json.dump(summary, f, indent=4)

print("\nDATASET SUMMARY")
print("-" * 40)
print(f"Dataset size: {summary['dataset_size']}")
for q, count in summary['quality_distribution'].items():
    print(f"{q.capitalize()}: {count}")

print("\nGENERATED STRUCTURE:")
print("-------------------")
print("dataset/")
print("  images/")
print("  metadata/")
print("\nAI-READY DATASET COMPLETE")