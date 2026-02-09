import dlt
import requests

@dlt.resource(
    write_disposition="merge",
    primary_key="id"
)
def remoteok_jobs():
    url = "https://remoteok.com/api"
    response = requests.get(url).json()

    for item in response:
        # Skip metadata / non-job entries
        if "id" not in item:
            continue
        yield item

pipeline = dlt.pipeline(
    pipeline_name="remoteok_loader",
    destination="duckdb",
    dataset_name="job_listings"
)

info = pipeline.run(remoteok_jobs())
print(info)
