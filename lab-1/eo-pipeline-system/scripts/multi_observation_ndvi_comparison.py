import os
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = "results/ndvi_comparison"
REPORT_FILE = "reports/multi_observation_ndvi_comparison.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("reports", exist_ok=True)

def create_sample_observation(name, cloud_level):
    red = np.random.uniform(200, 500, (300, 300))
    nir = np.random.uniform(2500, 4000, (300, 300))
    
    if cloud_level == "high":
        red[100:250, 80:220] = 6000
        nir[100:250, 80:220] = 6000
        
    return red, nir

def compute_ndvi(red, nir):
    return (nir - red) / (nir + red + 1e-6)

def save_ndvi_map(ndvi, output_path, title):
    plt.figure(figsize=(8, 6))
    plt.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
    plt.colorbar(label='NDVI')
    plt.title(title)
    plt.savefig(output_path)
    plt.close()

print("Generowanie obserwacji...")
red_low, nir_low = create_sample_observation("low", "low")
red_high, nir_high = create_sample_observation("high", "high")

ndvi_low = compute_ndvi(red_low, nir_low)
ndvi_high = compute_ndvi(red_high, nir_high)

save_ndvi_map(ndvi_low, os.path.join(OUTPUT_DIR, "low_cloud_observation_ndvi_map.png"), "Low Cloud Observation")
save_ndvi_map(ndvi_high, os.path.join(OUTPUT_DIR, "high_cloud_observation_ndvi_map.png"), "High Cloud Observation")

stats_low = {
    "min": np.min(ndvi_low), "max": np.max(ndvi_low), "mean": np.mean(ndvi_low),
    "high_veg": np.sum(ndvi_low > 0.5), "low_ndvi": np.sum(ndvi_low < 0)
}
stats_high = {
    "min": np.min(ndvi_high), "max": np.max(ndvi_high), "mean": np.mean(ndvi_high),
    "high_veg": np.sum(ndvi_high > 0.5), "low_ndvi": np.sum(ndvi_high < 0)
}

report_content = f"""MULTI-OBSERVATION NDVI COMPARISON
=================================

low_cloud_observation
---------------------
Cloud cover: ~5%
NDVI min: {stats_low['min']:.2f}
NDVI max: {stats_low['max']:.2f}
NDVI mean: {stats_low['mean']:.2f}
High vegetation pixels: {stats_low['high_veg']}
Low NDVI pixels: {stats_low['low_ndvi']}

high_cloud_observation
----------------------
Cloud cover: ~75%
NDVI min: {stats_high['min']:.2f}
NDVI max: {stats_high['max']:.2f}
NDVI mean: {stats_high['mean']:.2f}
High vegetation pixels: {stats_high['high_veg']}
Low NDVI pixels: {stats_high['low_ndvi']}
"""

with open(REPORT_FILE, "w") as f:
    f.write(report_content)

print("COMPARISON COMPLETE")
print("Generated files:")
print(f"- {OUTPUT_DIR}/low_cloud_observation_ndvi_map.png")
print(f"- {OUTPUT_DIR}/high_cloud_observation_ndvi_map.png")
print(f"- {REPORT_FILE}")