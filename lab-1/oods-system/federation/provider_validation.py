import json
import requests

with open("contracts/providers_registry.json", "r") as f:
    providers = json.load(f)

with open("contracts/observation_schema.json", "r") as f:
    contract = json.load(f)

required_fields = contract["required_fields"]

status_counts = {
    "OK": 0,
    "VIOLATION": 0,
    "UNAVAILABLE": 0,
    "EMPTY DATASET": 0
}
problematic_providers = []

for provider in providers:
    p_name = provider["name"]
    p_url = provider["url"]

    try:
        response = requests.get(f"{p_url}/observations", timeout=2)

        if response.status_code == 200:
            data = response.json()

            if len(data) == 0:
                print(f"{p_name}: EMPTY DATASET")
                status_counts["EMPTY DATASET"] += 1
                problematic_providers.append(p_name)
                continue

            missing = [field for field in required_fields if field not in data[0]]

            if missing:
                print(f"{p_name}: VIOLATION")
                print(f"  Missing fields: {missing}")
                status_counts["VIOLATION"] += 1
                problematic_providers.append(p_name)
            else:
                print(f"{p_name}: OK")
                status_counts["OK"] += 1
        else:
            print(f"{p_name}: UNAVAILABLE")
            status_counts["UNAVAILABLE"] += 1
            problematic_providers.append(p_name)

    except requests.exceptions.RequestException:
        print(f"{p_name}: UNAVAILABLE")
        status_counts["UNAVAILABLE"] += 1
        problematic_providers.append(p_name)

print("\nSUMMARY:")
for status, count in status_counts.items():
    print(f"{status}: {count}")

if problematic_providers:
    print("\nPROBLEMATIC PROVIDERS:")
    for name in problematic_providers:
        print(name)
    print("\nFEDERATION STATE: DEGRADED")
else:
    print("\nFEDERATION STATE: RELIABLE")
