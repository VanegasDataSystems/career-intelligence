"""Create DuckDB views for job listings."""

from pathlib import Path

import duckdb


def create_job_views(db_path, sql_path):
    conn = duckdb.connect(str(db_path))
    sql = sql_path.read_text()
    conn.execute(sql)
    conn.close()
    print(f"Views created successfully in {db_path}")


if __name__ == "__main__":
    BASE_PATH = Path(__file__).parent
    DB_PATH = BASE_PATH / "remoteok_loader.duckdb"
    SQL_PATH = BASE_PATH / "sql" / "create_views.sql"
    create_job_views(DB_PATH, SQL_PATH)
