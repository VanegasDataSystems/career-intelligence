import dlt
import requests
from pathlib import Path
from create_views import create_job_views

def main():
    # retains data from past extractions while loading new data
    @dlt.resource(write_disposition="merge", primary_key="id")
    def remoteok_jobs():
        url = "https://remoteok.com/api"
        response = requests.get(url).json()
        for item in response:
            # the first entry is not a job listing
            if "legal" in item or "id" not in item:
                continue
            yield item

    pipeline = dlt.pipeline(
        pipeline_name="remoteok_loader",
        destination=dlt.destinations.duckdb(str(DB_PATH)),
        dataset_name="job_listings"
    )

    info = pipeline.run(remoteok_jobs())
    print(info)
    print('\npipeline finished; creating views...')
    sql_file_path = SCRIPT_DIR / "sql" / "create_views.sql"

    create_job_views(DB_PATH, sql_file_path)

if __name__ == "__main__":
    SCRIPT_DIR = Path(__file__).parent
    DB_PATH = SCRIPT_DIR / "remoteok_loader.duckdb"

    main()
