import dataclasses


@dataclasses.dataclass
class JobListing:
    job_id: str
    position: str
    company: str
    location: str
    salary_min: int | None
    salary_max: int | None
    date: str
    url: str
    tags: str