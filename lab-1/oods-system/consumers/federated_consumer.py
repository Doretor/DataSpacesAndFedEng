import requests
import time
import json

try:
    with open("../contracts/providers_registry.json", "r") as f:
        expected_providers = [p["name"] for p in json.load(f)]
except FileNotFoundError:
    print("Nie znaleziono pliku contracts/providers_registry.json!")
    expected_providers = []

BROKER_EVENTS_URL = "http://127.0.0.1:7000/events"

print(f"STARTING CONSUMER...")
print(f"EXPECTED PROVIDERS: {expected_providers}\n")

while True:
    try:
        response = requests.get(BROKER_EVENTS_URL)
        events = response.json()
        
        print("CURRENT NUMBER OF EVENTS:", len(events))
        
        active_providers = sorted(set(event.get("provider") for event in events if "provider" in event))
        objects = sorted(set(event.get("object_id") for event in events if "object_id" in event))
        
        print("ACTIVE PROVIDERS:", active_providers)
        
        missing_providers = sorted(list(set(expected_providers) - set(active_providers)))
        is_complete = "NO" if missing_providers else "YES"
        
        if missing_providers:
            print("MISSING PROVIDERS:", missing_providers)
        else:
            print("MISSING PROVIDERS: ['none']")
            
        print("COMPLETE:", is_complete)
        print("OBSERVED OBJECTS:", objects)

        per_provider = {}
        latest_timestamp = ""
        
        for event in events:
            provider = event.get("provider")
            if provider:
                per_provider[provider] = per_provider.get(provider, 0) + 1
            
            ts = event.get("timestamp", "")
            if ts > latest_timestamp:
                latest_timestamp = ts

        selected_object = "OBJ-003"
        selected_count = sum(1 for event in events if event.get("object_id") == selected_object)
        
        print("PER PROVIDER:")
        for p, count in per_provider.items():
            print(f"{p}: {count}")
            
        print("DISTINCT OBJECTS:", len(objects))
        print(f"{selected_object} OBSERVATIONS:", selected_count)
        print("MOST RECENT TIMESTAMP:", latest_timestamp)
        
        print("-" * 40)
        
    except requests.exceptions.RequestException:
        print("Waiting for broker to be available...")
        
    time.sleep(3)
