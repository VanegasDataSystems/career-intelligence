import duckdb

path = "jobs.duckdb"

def get_connection():
    return duckdb.connect(path)

def insert_job(job):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO jobs (
            job_id,
            job_url,
            title,
            company,
            loc,
            salary,
            description,
            ts
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job["job_id"],
            job["job_url"],
            job["title"],
            job["company"],
            job["location"],
            job["salary"],
            job["description"],
            job["ts"],
        )
    )
    conn.close()