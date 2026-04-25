import json
import requests
import pandas as pd
import duckdb
from datetime import datetime
import os

with open("contracts/providers_registry.json", "r") as f:
    providers = json.load(f)

with open("contracts/observation_schema.json", "r") as f:
    contract = json.load(f)

req_fields = contract["required_fields"]

statuses = {}
validations = {}
all_data = []

for p in providers:
    name = p["name"]
    url = p["url"]
    try:
        resp = requests.get(f"{url}/observations", timeout=2)
        if resp.status_code == 200:
            statuses[name] = "AVAILABLE"
            data = resp.json()
            if len(data) > 0:
                missing = [f for f in req_fields if f not in data[0]]
                validations[name] = "VIOLATION" if missing else "OK"
                for r in data:
                    r["provider"] = name
                    all_data.append(r)
            else:
                validations[name] = "EMPTY"
        else:
            statuses[name] = "UNAVAILABLE"
            validations[name] = "UNAVAILABLE"
    except:
        statuses[name] = "UNAVAILABLE"
        validations[name] = "UNAVAILABLE"

total_obs = len(all_data)
distinct_objs = len(set(d.get("object_id") for d in all_data))

obj_id = "OBJ-003"
obj_data = [d for d in all_data if d.get("object_id") == obj_id]
obj_providers = list(set(d["provider"] for d in obj_data))

rest_res = total_obs

try:
    df_a = pd.read_json('http://127.0.0.1:8001/observations')
    df_b = pd.read_json('http://127.0.0.1:8002/observations')
    df_g = pd.read_json('http://127.0.0.1:8003/observations')
    query = "SELECT * FROM df_a UNION ALL SELECT * FROM df_b UNION ALL SELECT * FROM df_g"
    con = duckdb.connect(database=':memory:')
    df = con.execute(query).fetchdf()
    duckdb_res = len(df)
except:
    duckdb_res = "ERROR"

try:
    gql_query = {"query": "{ observations { provider } }"}
    gql_resp = requests.post("http://127.0.0.1:9000/graphql", json=gql_query, timeout=2)
    if gql_resp.status_code == 200:
        gql_res = len(gql_resp.json()["data"]["observations"])
    else:
        gql_res = "ERROR"
except:
    gql_res = "ERROR"

completeness = "YES" if all(v == "OK" for v in validations.values()) and all(s == "AVAILABLE" for s in statuses.values()) else "NO"

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
file_ts = datetime.now().strftime("%Y%m%d_%H%M%S")

report = f"""FEDERATED ACCESS REPORT
-----------------------
Generated at: {timestamp}

[REGISTERED PROVIDERS]
"""
for p in providers:
    report += f"- {p['name']}\n"

report += "\n[PROVIDER STATUS]\n"
for p, s in statuses.items():
    report += f"{p}: {s}\n"

report += "\n[CONTRACT VALIDATION]\n"
for p, v in validations.items():
    report += f"{p}: {v}\n"

report += f"""
[GLOBAL STATISTICS]
Total observations: {total_obs}
Distinct objects: {distinct_objs}

[OBJECT ANALYSIS: {obj_id}]
Providers containing object:
"""
for p in obj_providers:
    report += f"- {p}\n"

report += f"""Total observations: {len(obj_data)}

[ACCESS LAYERS]
REST RESULT: {rest_res}
DUCKDB RESULT: {duckdb_res}
GRAPHQL RESULT: {gql_res}

[COMPLETENESS]
Federation complete: {completeness}
"""

print(report)

os.makedirs("reports", exist_ok=True)
with open(f"reports/federated_access_report_{file_ts}.txt", "w") as f:
    f.write(report)
