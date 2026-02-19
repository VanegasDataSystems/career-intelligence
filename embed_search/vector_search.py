import json
import duckdb
from sentence_transformers import SentenceTransformer
from pathlib import Path


def main():
    TOP_K = 10
    OUTPUT_FILE = Path("search_results_jobs.json")

    # -------------------------------
    # User input
    # -------------------------------
    role_query = input("Enter job role / description: ").strip()
    if not role_query:
        print("Role query is required.")
        return

    location_filter = input("Enter location (optional, e.g. Texas): ").strip()

    # -------------------------------
    # Load embedding model (offline)
    # -------------------------------
    model = SentenceTransformer("models/all-MiniLM-L6-v2")

    query_embedding = model.encode(
        role_query,
        normalize_embeddings=True
    ).tolist()

    # -------------------------------
    # Connect to DuckDB
    # -------------------------------
    con = duckdb.connect("fv/remoteok_loader.duckdb")
    con.execute("use job_listings")
    con.execute("LOAD vss;")

    # -------------------------------
    # Build SQL with optional location filter
    # -------------------------------
    sql = """
        SELECT
            e.job_id,
            j.position,
            j.company,
            j.location,
            j.url,
            list_dot_product(e.embedding, ?) AS score
        FROM job_embeddings e
        JOIN remoteok_jobs j
            ON e.job_id = j.id
        WHERE 1=1
    """

    params = [query_embedding]

    if location_filter:
        sql += " AND lower(j.location) LIKE ?"
        params.append(f"%{location_filter.lower()}%")

    sql += """
        ORDER BY score DESC
        LIMIT ?
    """
    params.append(TOP_K)

    results = con.execute(sql, params).fetchall()

    if not results:
        print("No matching jobs found.")
        return

    # -------------------------------
    # Load existing searches (append-only)
    # -------------------------------
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            searches = json.load(f)
    else:
        searches = []

    search_id = len(searches) + 1

    search_entry = {
        "search_id": search_id,
        "role_query": role_query,
        "location_filter": location_filter,
        "jobs": [
            {
                "job_id": int(job_id),
                "title": title,
                "company": company,
                "location": location,
                "score": round(score, 4),
                "url": url
            }
            for job_id, title, company, location, url, score in results
        ]
    }

    searches.append(search_entry)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(searches, f, indent=2)

    # -------------------------------
    # Console output
    # -------------------------------
    print(f"\nSearch {search_id} saved to {OUTPUT_FILE}")
    print("Top matching jobs:\n")

    for i, job in enumerate(search_entry["jobs"], start=1):
        print(f"{i}. {job['title']} — {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Score: {job['score']}\n")


if __name__ == "__main__":
    main()
