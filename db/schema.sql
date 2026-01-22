create table if not exists jobs(
    job_id TEXT, 
    job_url TEXT, 
    title TEXT, 
    company TEXT, 
    loc TEXT, 
    salary TEXT, 
    description TEXT, 
    ts TIMESTAMP
);