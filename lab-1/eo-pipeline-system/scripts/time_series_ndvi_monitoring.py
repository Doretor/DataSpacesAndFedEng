import os
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = "results/ndvi_timeseries"
REPORT_FILE = "reports/time_series_ndvi_monitoring.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("reports", exist_ok=True)

def create_sample_observation(name, nir_base_level):
    red = np.random.uniform(1800, 2200, (300, 300))
    nir = np.random.uniform(nir_base_level - 200, nir_base_level + 200, (300, 300))
    return red, nir

def compute_ndvi(red, nir):
    return (nir - red) / (nir + red + 1e-6)

def save_ndvi_map(ndvi, output_path, title):
    plt.figure(figsize=(8, 6))
    plt.imshow(ndvi, cmap='RdYlGn', vmin=-0.2, vmax=1.0)
    plt.colorbar(label='NDVI')
    plt.title(title)
    plt.savefig(output_path)
    plt.close()

observations = [
    {"name": "2024-04-01", "nir_level": 2600},
    {"name": "2024-05-01", "nir_level": 3400},
    {"name": "2024-06-01", "nir_level": 4300}
]

dates = []
mean_values = []
report_lines = ["TIME-SERIES NDVI MONITORING REPORT", "="*34]

print("TIME-SERIES NDVI MONITORING")
print("==================================================")

for obs in observations:
    date = obs["name"]
    print(f"Processing: observation_{date}")
    
    red, nir = create_sample_observation(date, obs["nir_level"])
    ndvi = compute_ndvi(red, nir)
    
    mean_ndvi = np.mean(ndvi)
    dates.append(date)
    mean_values.append(mean_ndvi)
    
    print(f"Mean NDVI: {mean_ndvi:.2f}")
    report_lines.append(f"\n{date}")
    report_lines.append(f"Mean NDVI: {mean_ndvi:.2f}")
    
    map_path = os.path.join(OUTPUT_DIR, f"observation_{date}_ndvi_map.png")
    save_ndvi_map(ndvi, map_path, f"NDVI Map - {date}")

trend_plot_path = os.path.join(OUTPUT_DIR, "mean_ndvi_trend.png")
plt.figure(figsize=(8, 5))
plt.plot(dates, mean_values, marker="o", linestyle="-", color="green", markersize=8)
plt.title("Mean NDVI Trend (Apr - Jun)")
plt.xlabel("Date")
plt.ylabel("Mean NDVI")
plt.grid(True, linestyle="--", alpha=0.7)
plt.savefig(trend_plot_path)
plt.close()

first_mean = mean_values[0]
last_mean = mean_values[-1]
change = last_mean - first_mean

if change > 0.05:
    trend = "Increasing vegetation activity"
elif change < -0.05:
    trend = "Decreasing vegetation activity"
else:
    trend = "Stable vegetation conditions"

report_lines.append("\nVegetation trend:")
report_lines.append("-----------------")
report_lines.append(f"First mean NDVI: {first_mean:.2f}")
report_lines.append(f"Last mean NDVI: {last_mean:.2f}")
report_lines.append(f"Change: {change:+.2f}")
report_lines.append("Detected trend:")
report_lines.append(trend)

with open(REPORT_FILE, "w") as f:
    f.write("\n".join(report_lines))

print("\nTIME-SERIES NDVI MONITORING COMPLETE")
print("Generated files:")
print(f"  {OUTPUT_DIR}/observation_2024_04_01_ndvi_map.png")
print(f"  {OUTPUT_DIR}/observation_2024_05_01_ndvi_map.png")
print(f"  {OUTPUT_DIR}/observation_2024_06_01_ndvi_map.png")
print(f"  {trend_plot_path}")
print(f"  {REPORT_FILE}")