"""Create DuckDB views for job listings."""

from pathlib import Path

import duckdb

DB_PATH = Path(__file__).parent / "remoteok_loader.duckdb"
SQL_PATH = Path(__file__).parent / "sql" / "create_views.sql"


def main():
    conn = duckdb.connect(str(DB_PATH))
    sql = SQL_PATH.read_text()
    conn.execute(sql)
    conn.close()
    print(f"Views created successfully in {DB_PATH}")


if __name__ == "__main__":
    main()
