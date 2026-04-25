import duckdb
import pandas as pd

df_a = pd.read_json('http://127.0.0.1:8001/observations')
df_b = pd.read_json('http://127.0.0.1:8002/observations')
df_g = pd.read_json('http://127.0.0.1:8003/observations')

query = """
SELECT 'satellite_A' AS provider, * FROM df_a
UNION ALL
SELECT 'satellite_B' AS provider, * FROM df_b
UNION ALL
SELECT 'ground_station' AS provider, * FROM df_g
"""

con = duckdb.connect(database=':memory:')
df = con.execute(query).fetchdf()

total_obs = len(df)
obj_003_obs = len(df[df['object_id'] == 'OBJ-003'])
provider_counts = df['provider'].value_counts()
largest_provider = provider_counts.idxmax()

print(f"TOTAL OBSERVATIONS: {total_obs}")
print(f"OBJ-003 OBSERVATIONS: {obj_003_obs}\n")

for provider, count in provider_counts.items():
    print(f"{provider}: {count}")

print("\nLARGEST PROVIDER:")
print(largest_provider)
