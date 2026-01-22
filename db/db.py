import duckdb

path = "jobs.duckdb"

def get_connection():
    return duckdb.connect(path)