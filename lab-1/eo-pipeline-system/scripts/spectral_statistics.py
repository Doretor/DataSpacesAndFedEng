import os
import rasterio
import numpy as np

RASTER_FILES = {
    "B04_10m": "assets/bands/B04_10m.tif",
    "B08_10m": "assets/bands/B08_10m.tif"
}

os.makedirs("reports", exist_ok=True)
report_lines = ["RAPORT STATYSTYK SPEKTRALNYCH", "="*50]

for name, path in RASTER_FILES.items():
    print("=" * 50)
    print(name)
    report_lines.append(f"\n{'=' * 50}\n{name}")

    if not os.path.exists(path):
        msg = f"SKIPPED: File {path} not found."
        print(msg)
        report_lines.append(msg)
        continue

    with rasterio.open(path) as src:
        band = src.read(1)
        
        b_min = np.min(band)
        b_max = np.max(band)
        b_mean = np.mean(band)
        b_std = np.std(band)

        print(f"MIN:  {b_min:.2f}")
        print(f"MAX:  {b_max:.2f}")
        print(f"MEAN: {b_mean:.2f}")
        print(f"STD:  {b_std:.2f}")

        report_lines.append(f"MIN:  {b_min:.2f}")
        report_lines.append(f"MAX:  {b_max:.2f}")
        report_lines.append(f"MEAN: {b_mean:.2f}")
        report_lines.append(f"STD:  {b_std:.2f}")

with open("reports/spectral_statistics.txt", "w") as f:
    f.write("\n".join(report_lines))

print("\nRaport zapisano w: reports/spectral_statistics.txt")