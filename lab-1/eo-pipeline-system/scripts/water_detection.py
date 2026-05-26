import os
import numpy as np
import matplotlib.pyplot as plt

NDVI_PATH = "results/ndvi/ndvi.npy"
MASK_OUTPUT = "results/ndvi/water_mask.png"
REPORT_FILE = "reports/water_detection.txt"

if not os.path.exists(NDVI_PATH):
    print(f"BŁĄD: Nie znaleziono {NDVI_PATH}. Uruchom Task 5.")
    exit(1)

print("WATER DETECTION")
print("==================================================")
print("Loading NDVI...")

ndvi = np.load(NDVI_PATH)
print(f"NDVI shape: {ndvi.shape}")

print("Generating binary mask...")
water_mask = ndvi < 0

total_pixels = ndvi.size
water_pixels = np.sum(water_mask)
non_water_pixels = total_pixels - water_pixels
water_percentage = (water_pixels / total_pixels) * 100

print(f"Water candidate pixels: {water_pixels}")
print(f"Non-water pixels: {non_water_pixels}")

plt.figure(figsize=(10, 8))
plt.imshow(water_mask, cmap='Blues')
plt.colorbar(label='Water Candidate (1 = Yes, 0 = No)')
plt.title('Binary Water Mask (NDVI < 0)')
plt.savefig(MASK_OUTPUT)
plt.close()

report_content = f"""WATER DETECTION REPORT
======================
Detection rule:
NDVI < 0

Pixel statistics:
Water candidate pixels: {water_pixels}
Non-water pixels: {non_water_pixels}
Water candidate percentage: {water_percentage:.2f}%
"""

with open(REPORT_FILE, "w") as f:
    f.write(report_content)

print("FILES GENERATED:")
print("----------------")
print(MASK_OUTPUT)
print(REPORT_FILE)