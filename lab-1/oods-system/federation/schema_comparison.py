import json
import requests

with open("contracts/providers_registry.json", "r") as f:
    providers = json.load(f)

urls = {}
for p in providers:
    urls[p["name"]] = p["url"]

data_a = requests.get(f"{urls.get('satellite_A')}/observations").json()
data_b = requests.get(f"{urls.get('satellite_B')}/observations").json()

tot_a = len(data_a)
obj_a = sum(1 for item in data_a if item.get("object_id") == "OBJ-003")

tot_b = len(data_b)
obj_b = sum(1 for item in data_b if item.get("object_id") == "OBJ-003")

print("satellite_A:")
print(f"TOTAL OBSERVATIONS: {tot_a}")
print(f"OBJ-003 OBSERVATIONS: {obj_a}")

print("\nsatellite_B:")
print(f"TOTAL OBSERVATIONS: {tot_b}")
print(f"OBJ-003 OBSERVATIONS: {obj_b}")

print("\nSCHEMA COMPARISON:")

keys_a = set(data_a[0].keys()) if tot_a > 0 else set()
keys_b = set(data_b[0].keys()) if tot_b > 0 else set()

if keys_a == keys_b and len(keys_a) > 0:
    print("satellite_A and satellite_B are compatible")
else:
    print("satellite_A and satellite_B are NOT compatible")
