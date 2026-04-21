import json
import requests
with open("./contracts/providers_registry.json", "r") as f:
	providers = json.load(f)

all_results = []
provider_counts = {}

for provider in providers:
	provider_name = provider["name"]
	provider_url = provider["url"]
	response = requests.get(f"{provider_url}/observations")
	data = response.json()
	provider_counts[provider_name] = len(data)
	for row in data:
		row["provider"] = provider_name
		all_results.append(row)

print("TOTAL RECORDS:", len(all_results))

print("\nPRE-PROVIDER COUNTS:")

for name, count in provider_counts.items():
	print(f"{name}: {count}")

largest_provider=max(provider_counts, key=provider_counts.get)
print(f"\nLARGEST PROVIDER:\n{largest_provider}")

