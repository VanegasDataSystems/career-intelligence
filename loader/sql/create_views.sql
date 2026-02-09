CREATE OR REPLACE VIEW job_listings.jobs_with_tags AS
SELECT j.id as job_id, j.salary_min, j.salary_max, j.location, j.position, j.company, j.date, j.url,
       count(t.value) as tag_count,
       STRING_AGG(t.value, ', ') AS tags
FROM job_listings.remoteok_jobs j
LEFT OUTER JOIN job_listings.remoteok_jobs__tags t
ON j."_dlt_id" = t."_dlt_parent_id"
GROUP BY ALL;
