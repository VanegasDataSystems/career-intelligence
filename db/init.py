import duckdb

conn = duckdb.connect("jobs.duckdb")

with open("db/schema.sql", "r") as f:
    schema = f.read()

conn.execute(schema)
conn.close()

print("initialized")