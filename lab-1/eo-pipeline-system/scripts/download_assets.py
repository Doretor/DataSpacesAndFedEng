import os
import requests

STAC_URL = "https://stac.dataspace.copernicus.eu/v1/search"
QUERY = {
    "collections": ["sentinel-2-l2a"],
    "bbox": [19.0, 50.0, 20.0, 51.0],
    "datetime": "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z",
    "query": {
        "eo:cloud_cover": {
            "lt": 20
        }
    },
    "limit": 1
}

OUTPUT_PATHS = {
    "thumbnail": "assets/thumbnails/thumbnail.jpg",
    "TCI_10m": "assets/visual/visual.jp2",
    "B04_10m": "assets/bands/B04.jp2",
    "B08_10m": "assets/bands/B08.jp2"
}

def is_http_url(url):
    return url.startswith("http://") or url.startswith("https://")

def download_file(url, output_path):
    if not is_http_url(url):
        print("SKIPPED NON-HTTP ASSET:", url)
        return False
    
    print(f"Pobieranie {url} do {output_path}...")
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return True

print("Wysyłanie zapytania do STAC API...")
response = requests.post(STAC_URL, json=QUERY)
data = response.json()
item = data["features"][0]
assets = item["assets"]

print("\nDOSTĘPNE ASSETY:")
for asset_name in assets:
    print(f"- {asset_name}")

print("\n--- ROZPOCZĘCIE POBIERANIA ---")
downloaded_count = 0
skipped_count = 0

for asset_key, output_path in OUTPUT_PATHS.items():
    if asset_key in assets:
        asset_url = assets[asset_key]["href"]
        success = download_file(asset_url, output_path)
        if success:
            downloaded_count += 1
        else:
            skipped_count += 1
    else:
        print(f"Brak pliku '{asset_key}' w metadanych.")
        skipped_count += 1

report = f"""RAPORT Z POBIERANIA ASSETÓW
---------------------------
Wymagane pliki: {len(OUTPUT_PATHS)}
Pomyślnie pobrano: {downloaded_count}
Pominięto (S3 lub brak): {skipped_count}
"""

print("\n" + report)
with open("reports/download_report.txt", "w") as f:
    f.write(report)