import requests
import time
import json

with open("../contracts/event_schema.json", "r") as f:
	contract = json.load(f)


BROKER_EVENTS_URL = "http://127.0.0.1:7000/events"

while True:
	response = requests.get(BROKER_EVENTS_URL)
	events = response.json()

	required_fields = contract["required_fields"]
	valid_count = 0
	invalid_count = 0
	missing = ""
	for event in events:
		missing = [field for field in required_fields if field not in event]
		if missing:
			print("INVALID EVENT:", event)
			print("MISSING FIELDS:", missing)
			invalid_count += 1
		else:
			valid_count += 1
	print("VALID EVENTS:", valid_count)
	print("INVALID EVENTS:", invalid_count)
	print(f"\nINVALID EVENT DETECTED:\nMissing fields: {missing}")
	print("-"*40)
	time.sleep(3)



