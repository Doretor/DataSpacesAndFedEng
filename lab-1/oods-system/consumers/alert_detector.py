import requests
import time

BROKER_EVENTS_URL = "http://127.0.0.1:7000/events"
TARGET_OBJECT = "OBJ-003"

print(f"STARTING ALERT DETECTOR FOR: {TARGET_OBJECT}...\n")

processed_events_count = 0

while True:
    try:
        response = requests.get(BROKER_EVENTS_URL)
        events = response.json()
        
        new_events = events[processed_events_count:]
        
        for event in new_events:
            if event.get("object_id") == TARGET_OBJECT:
                provider = event.get("provider", "Unknown")
                timestamp = event.get("timestamp", "Unknown")
                print(f"ALERT: {TARGET_OBJECT} observed by {provider} at {timestamp}")
        
        processed_events_count = len(events)
        
    except requests.exceptions.RequestException:
        print("Waiting for broker...")
        
    time.sleep(2)
