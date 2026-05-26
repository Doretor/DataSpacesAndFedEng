import os
import rasterio

RASTER_FILES = [
    "assets/visual/visual.jp2",
    "assets/bands/B04_10m.tif",
    "assets/bands/B08_10m.tif"
]

report_lines = ["INSPEKCJA RASTROW (RASTER INSPECTION)", "="*50]

for raster_path in RASTER_FILES:
    report_lines.append(f"\nFile: {raster_path}")
    print("="*50)
    print(raster_path)
    
    if not os.path.exists(raster_path):
        msg = "SKIPPED: File does not exist."
        print(msg)
        report_lines.append(msg)
        continue
        
    try:
        with rasterio.open(raster_path) as src:
            width = src.width
            height = src.height
            bands = src.count
            crs = src.crs
            bounds = src.bounds
            
            print(f"Width: {width}")
            print(f"Height: {height}")
            print(f"Bands: {bands}")
            print(f"CRS: {crs}")
            print(f"Bounds: {bounds}")
            
            report_lines.append(f"Width: {width}")
            report_lines.append(f"Height: {height}")
            report_lines.append(f"Bands: {bands}")
            report_lines.append(f"CRS: {crs}")
            report_lines.append(f"Bounds: {bounds}")
  
    except Exception as e:
        msg = f"ERROR reading raster: {e}"
        print(msg)
        report_lines.append(msg)

os.makedirs("reports", exist_ok=True)
with open("reports/raster_inspection.txt", "w") as f:
    f.write("\n".join(report_lines))

print("\n==================================================")
print("Raport został zapisany w pliku: reports/raster_inspection.txt")
