import dlt
import feedparser

@dlt.resource(write_disposition="replace")
def wwr_jobs_resource():
    url = "https://weworkremotely.com/remote-jobs.rss"
    feed = feedparser.parse(url)

    for entry in feed.entries:
        raw_tags = entry.get('tags', [])
        clean_tags = [{'term': t['term']} for t in raw_tags if 'term' in t]

        yield {
            "remote_id": entry.id,
            "title": entry.title,
            "url": entry.link,
            "posted_at": entry.published,
            "description": entry.description,
            "region": entry.get("region"),
            "job_type": entry.get("type"),
            "skills": entry.get("skills"),
            "tags": clean_tags,
            "source": "WeWorkRemotely"
        }


pipeline = dlt.pipeline(
    pipeline_name="wwr_loader",
    destination="duckdb",
    dataset_name="wwr_listings"
)

info = pipeline.run(wwr_jobs_resource())
print(info)