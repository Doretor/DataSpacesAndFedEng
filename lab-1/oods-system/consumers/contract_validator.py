import requests
import time
import json
import sys

try:
    with open("../contracts/event_schema.json", "r") as f:
        contract = json.load(f)
        required_fields = contract["required_fields"]
except FileNotFoundError:
    print("Błąd: Nie znaleziono pliku contracts/event_schema.json!")
    sys.exit(1)

BROKER_EVENTS_URL = "http://127.0.0.1:7000/events"

print("STARTING CONTRACT VALIDATOR...\n")

while True:
    try:
        response = requests.get(BROKER_EVENTS_URL)
        events = response.json()

        valid_count = 0
        invalid_count = 0
        invalid_details = []

        for event in events:
            missing = [field for field in required_fields if field not in event]
            
            if missing:
                invalid_count += 1
                invalid_details.append(missing)
            else:
                valid_count += 1

        print(f"VALID EVENTS: {valid_count}")
        print(f"INVALID EVENTS: {invalid_count}")
        
        for missing_fields in invalid_details:
            print("INVALID EVENT DETECTED:")
            print(f"Missing fields: {', '.join(missing_fields)}")
            
        print("-" * 40)

    except requests.exceptions.RequestException:
        print("Waiting for broker to be available...")

    time.sleep(3)
