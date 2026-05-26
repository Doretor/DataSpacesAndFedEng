import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("results/ndvi", exist_ok=True)
os.makedirs("reports", exist_ok=True)

print("Rozpoczynam obliczanie wskaźnika NDVI...")

with rasterio.open("assets/bands/B04_10m.tif") as red_src:
    red = red_src.read(1).astype(float)

with rasterio.open("assets/bands/B08_10m.tif") as nir_src:
    nir = nir_src.read(1).astype(float)

ndvi = (nir - red) / (nir + red + 1e-6)

ndvi_min = np.min(ndvi)
ndvi_max = np.max(ndvi)
ndvi_mean = np.mean(ndvi)

high_veg_pixels = np.sum(ndvi > 0.5)
low_ndvi_pixels = np.sum(ndvi < 0)

print(f"NDVI MIN: {ndvi_min:.2f}")
print(f"NDVI MAX: {ndvi_max:.2f}")
print(f"NDVI MEAN: {ndvi_mean:.2f}")
print(f"Piksele o wysokiej roślinności (NDVI > 0.5): {high_veg_pixels}")
print(f"Piksele o niskim NDVI (woda/cienie) (NDVI < 0): {low_ndvi_pixels}")

np.save("results/ndvi/ndvi.npy", ndvi)
print("\n[ZAPISANO] Macierz NDVI: results/ndvi/ndvi.npy")

plt.figure(figsize=(8, 6))
plt.imshow(ndvi, cmap='RdYlGn')
plt.colorbar(label='Wartość NDVI')
plt.title('Mapa NDVI')
plt.savefig("results/ndvi/ndvi_map.png")
plt.close()
print("[ZAPISANO] Mapa NDVI: results/ndvi/ndvi_map.png")

report = f"""RAPORT NDVI
=========================
NDVI MIN: {ndvi_min:.2f}
NDVI MAX: {ndvi_max:.2f}
NDVI MEAN: {ndvi_mean:.2f}
High vegetation pixels: {high_veg_pixels}
Low NDVI pixels: {low_ndvi_pixels}
"""

with open("reports/ndvi_report.txt", "w") as f:
    f.write(report)
print("[ZAPISANO] Raport: reports/ndvi_report.txt")