import os
import numpy as np
import matplotlib.pyplot as plt

NDVI_PATH = "results/ndvi/ndvi.npy"
OUTPUT_IMAGE = "results/ndvi/ndvi_map.png"
REPORT_FILE = "reports/ndvi_analysis.txt"

os.makedirs("results/ndvi", exist_ok=True)
os.makedirs("reports", exist_ok=True)

if not os.path.exists(NDVI_PATH):
    print(f"ERROR: Nie znaleziono pliku {NDVI_PATH}. Uruchom najpierw Task 5.")
    exit(1)

ndvi = np.load(NDVI_PATH)

ndvi_min = np.min(ndvi)
ndvi_max = np.max(ndvi)
ndvi_mean = np.mean(ndvi)
high_vegetation_pixels = np.sum(ndvi > 0.5)
low_ndvi_pixels = np.sum(ndvi < 0)

plt.figure(figsize=(10, 8))
plt.imshow(ndvi, cmap='RdYlGn')
plt.colorbar(label='Wartość NDVI')
plt.title('Mapa NDVI')
plt.savefig(OUTPUT_IMAGE)
plt.close()

report_content = f"""NDVI VISUALIZATION
==========
NDVI MIN: {ndvi_min:.2f}
NDVI MAX: {ndvi_max:.2f}
NDVI MEAN: {ndvi_mean:.2f}
HIGH VEGETATION PIXELS: {high_vegetation_pixels}
LOW NDVI PIXELS: {low_ndvi_pixels}
NDVI MAP SAVED TO: {OUTPUT_IMAGE}
ANALYSIS REPORT SAVED TO: {REPORT_FILE}
"""

with open(REPORT_FILE, "w") as f:
    f.write(report_content)

print(report_content)