import json
import requests
with open("./contracts/providers_registry.json", "r") as f:
	providers = json.load(f)
object_id = "OBJ-003"
results = []
providers_with_object = []
all_providers = []
for provider in providers:
	provider_name = provider["name"]
	provider_url = provider["url"]
	response = requests.get(f"{provider_url}/observations/{object_id}")
	data = response.json()
	all_providers.append(provider_name)
	if data:
		providers_with_object.append(provider_name)
	for row in data:
		row["provider"] = provider_name
		results.append(row)

print("OBJECT:", object_id)
print("TOTAL OBSERVATIONS:", len(results))
print("PROVIDERS CONTAINING OBJECT:")
for name in providers_with_object:
	print(name)
