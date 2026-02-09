import json
import duckdb
from sentence_transformers import SentenceTransformer


def main():
    # Load cleaned job data
    with open("jobs_cleaned_with_skills.json", "r", encoding="utf-8") as f:
        jobs = json.load(f)

    job_ids = []
    descriptions = []

    for job in jobs:
        desc = job.get("description_clean", "")
        if desc.strip():
            job_ids.append(job["job_id"])
            descriptions.append(desc)

    total = len(descriptions)
    print(f"Total jobs to embed: {total}")

    # Load embedding model (local, offline)
    print("Loading embedding model...")
    model = SentenceTransformer("models/all-MiniLM-L6-v2")
    print("Model loaded.")

    # Generate embeddings
    print("Generating embeddings...")
    embeddings = model.encode(
        descriptions,
        batch_size=32,
        normalize_embeddings=True,
        show_progress_bar=True
    )
    print("Embedding generation complete.")

    # Connect to DuckDB
    print("Connecting to DuckDB...")
    con = duckdb.connect("fv/remoteok_loader.duckdb")
    con.execute("use job_listings")

    # Load VSS (already installed manually)
    con.execute("LOAD vss;")

    # Create embeddings table if it doesn't exist
    con.execute("""
        CREATE TABLE IF NOT EXISTS job_embeddings (
            job_id BIGINT PRIMARY KEY,
            embedding FLOAT[384]
        )
    """)

    # Store embeddings with progress
    print("Storing embeddings in database...")
    for i, (job_id, emb) in enumerate(zip(job_ids, embeddings), start=1):
        con.execute(
            "INSERT OR REPLACE INTO job_embeddings VALUES (?, ?)",
            [job_id, emb.tolist()]
        )

        if i % 50 == 0 or i == total:
            print(f"Stored {i} / {total} embeddings")

    print("All embeddings stored successfully.")


if __name__ == "__main__":
    main()
