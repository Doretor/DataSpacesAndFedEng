import requests
import os

os.makedirs("reports", exist_ok=True)

url = "https://stac.dataspace.copernicus.eu/v1/search"

query = {
    "collections": ["sentinel-2-l2a"],
    "bbox": [19.0, 50.0, 20.0, 51.0],
    "datetime": "2024-05-01T00:00:00Z/2024-05-10T23:59:59Z",
    "limit": 5
}

try:
    response = requests.post(url, json=query, timeout=20)
    response.raise_for_status()
    data = response.json()
    
    with open("reports/python_stac_results.txt", "w") as file:
        file.write("STAC PYTHON CLIENT RESULTS\n\n")
        
        for item in data.get("features", []):
            prod_id = item["id"]
            acq_time = item["properties"]["datetime"]
            
            parts = prod_id.split('_')
            satellite = parts[0] if len(parts) > 0 else "Unknown"
            tile = parts[5] if len(parts) > 5 else "Unknown"
            
            assets_count = len(item.get("assets", {}))
            
            file.write(f"Product ID: {prod_id}\n")
            file.write(f"Acquisition Time: {acq_time}\n")
            file.write(f"Satellite Name: {satellite}\n")
            file.write(f"Tile Identifier: {tile}\n")
            file.write(f"Available Assets: {assets_count}\n")
            file.write("-" * 40 + "\n")
            
except requests.exceptions.RequestException as e:
    print("REQUEST FAILED:", e)
except ValueError:
    print("INVALID JSON RESPONSE")
