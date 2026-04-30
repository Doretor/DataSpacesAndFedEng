import requests
import time

BROKER_EVENTS_URL = "http://127.0.0.1:7000/events"

print("STARTING DUPLICATE EVENT DETECTOR...\n")

seen_events = set()
processed_count = 0

while True:
    try:
        response = requests.get(BROKER_EVENTS_URL)
        events = response.json()
        
        new_events = events[processed_count:]
        
        for event in new_events:
            provider = event.get("provider")
            timestamp = event.get("timestamp")
            object_id = event.get("object_id")
            
            event_signature = (provider, timestamp, object_id)
            
            if event_signature in seen_events:
                print("DUPLICATE EVENT DETECTED:")
                print(f"provider={provider}")
                print(f"timestamp={timestamp}")
                print(f"object_id={object_id}")
                print("-" * 30)
            else:
                seen_events.add(event_signature)
        processed_count = len(events)
        
    except requests.exceptions.RequestException:
        print("Waiting for broker...")
        
    time.sleep(2)
