import duckdb

def main():
    con = duckdb.connect("fv/remoteok_loader.duckdb")
    con.execute("use job_listings")

    # 1. Check table exists and count rows
    result = con.execute(
        "SELECT COUNT(*) FROM job_embeddings"
    ).fetchone()
    print("Number of embeddings:", result[0])

    # 2. Check embedding dimension
    dim = con.execute(
        "SELECT array_length(embedding) FROM job_embeddings LIMIT 1"
    ).fetchone()
    print("Embedding dimension:", dim[0])

    # 3. Show a sample row
    sample = con.execute(
        "SELECT job_id, embedding[1:5] FROM job_embeddings LIMIT 1"
    ).fetchone()
    print("Sample job_id:", sample[0])
    print("First 5 values of embedding:", sample[1])

    # 4. Join with job table (sanity check)
    join_check = con.execute("""
        SELECT j.position, e.job_id
        FROM job_embeddings e
        JOIN remoteok_jobs j
        ON e.job_id = j.id
        LIMIT 5
    """).fetchall()

    print("\nJoin check (job title + id):")
    for row in join_check:
        print(row)

    print("\nDuckDB embedding verification done.")


if __name__ == "__main__":
    main()
