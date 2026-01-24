select j.id as job_id, j.salary_min, j.salary_max, j.location, j.position, j.company, j.date, j.url, count(t.value) as tagCount,
       STRING_AGG(t.value, ', ') AS tags_string
from job_listings.remoteok_jobs j

left outer join job_listings.remoteok_jobs__tags t
on j."_dlt_id" = t."_dlt_parent_id"
GROUP BY ALL