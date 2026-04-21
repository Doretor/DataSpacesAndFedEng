import requests

print("satellite_A:")

response = requests.get("http://127.0.0.1:8001/observations")
data = response.json()
print("NUMBER OF OBSERVATIONS:\n", len(data))

object_id = "OBJ-003"
response = requests.get(f"http://127.0.0.1:8001/observations/{object_id}")
dataA = response.json()
print(f"{object_id} RESULTS: {len(dataA)}\n")

object_id = "OBJ-003"
response = requests.get(f"http://127.0.0.1:8002/observations/{object_id}")
dataB = response.json()
print(f"{object_id} RESULTS: {len(dataB)}\n")

print("COMPARSION:")
if len(dataA)>0 and len(dataB)>0:
	print(f"{object_id} is present in both providers.")
elif len(dataA)>0:
	print(f"{object_id} is present only in satellite_A.")
elif len(dataB)>0:
	print(f"{object_id} is present only in satellite_B.")
else:
	print(f"{object_id} is not present in both providers.")
