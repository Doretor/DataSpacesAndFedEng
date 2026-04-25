import json
import requests

with open("./contracts/providers_registry.json", "r") as f:
    providers = json.load(f)

object_id = "OBJ-003"
results = []
providers_with_object = []

expected_providers = [p["name"] for p in providers]

for provider in providers:
    provider_name = provider["name"]
    provider_url = provider["url"]
    
    try:
        response = requests.get(f"{provider_url}/observations/{object_id}", timeout=2)
        
        if response.status_code == 200:
            data = response.json()
            
            if len(data) > 0:
                providers_with_object.append(provider_name)
                for row in data:
                    row["provider"] = provider_name
                    results.append(row)
    except Exception:
        pass

missing_providers = [name for name in expected_providers if name not in providers_with_object]

print(f"OBJECT: {object_id}")
print(f"TOTAL OBSERVATIONS: {len(results)}")

print("\nPROVIDERS CONTAINING OBJECT:")
for name in providers_with_object:
    print(name)

print("\nMISSING PROVIDERS:")
if len(missing_providers) == 0:
    print("none")
    print("\nCOMPLETENESS: YES")
else:
    for name in missing_providers:
        print(name)
    print("\nCOMPLETENESS: NO")
